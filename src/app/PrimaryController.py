import json
import os
import datetime

# https://pythonbasics.org/flask-upload-file/#:~:text=It%20is%20very%20simple%20to,it%20to%20the%20required%20location.
from werkzeug.utils import secure_filename

# integrate Flask API Class Libraries
from flask import Flask, jsonify, render_template, request, send_from_directory, redirect
from flask_classful import FlaskView, route

# integrate Database & MarvelController class controller
from DatabaseController import DatabaseController
from PDFController import PDFController

# Instantiate Supporting Classes
dbController = DatabaseController()
pdfController = PDFController()

# instantiate app instance
app = Flask(__name__)

# Controller Class To Integrate with UI, MarvelAPI Backend, Local Database.
class PrimaryController(FlaskView):

    def __init__(self) -> None:
        # Create a directory in a known location to save files to.
        self.uploads_dir = os.path.join(app.instance_path, 'uploads')
        os.makedirs(self.uploads_dir, exist_ok=True)

    # ROUTE #0: DISPLAY ALL TABLES (CHARACTERS) IN DATABASE AS CLICKABLE LINKS
    @route('/', methods=["GET"])
    def index(self):

        # gather homepage HTML into table
        indexHTML = render_template("index.html")

        # fetch records from database cache, display into table
        fileRecords = dbController.return_all_records_from_cache()

        # stage HTML placeholder for data/table records
        tableRecordsHTML = """"""

        # dynamically build table records based on file records from database
        for fileRecord in fileRecords:

            # build table row based on fileRecord
            tableRecordsHTML += """
                <tr>
                    <td>{}</td>
                    <td>{}</td>
                    <td>{}</td>
                    <td>{}</td>
                    <td>
                        <form action="http://localhost:5050/file/{}", method="GET">
                            <button type="submit" value="submit" class="btn btn-primary">
                                Click Here
                            </button>
                        </form>
                    </td>
                </tr>
            """.format(fileRecord["filename"], fileRecord["createdBy"], fileRecord["createdAt"], fileRecord["docType"], fileRecord["uuid"])

        # append table records to HTML Table, Replace Bearer Token
        indexHTML = indexHTML.replace("DYNAMIC-TABLE-CONTENT-REPLACED-HERE", tableRecordsHTML)
        indexHTML = indexHTML.replace("REPLACE-BEARER-TOKEN-HERE", os.environ['BEARER_TOKEN'])

        # read base-template
        return indexHTML

    # ROUTE #1: FETCH FILE FROM DATABASE BY ID. DISPLAY IN INDEX & RETURN METADATA IN HEADERS (UNIT TEST SUPPORT)
    @route('/file/<id>', methods=['GET'])
    def getTableData(self, id):

        # fetch records from cache
        recordFromCache = dbController.return_record_from_cache(id)

        # handle record not found in database
        if recordFromCache == None:
            notificationHTML = render_template("notification.html")
            return notificationHTML.replace("INSERT-MESSAGE-HERE","Requested File Not Found")
        else:

            # location for downloadable file path
            path = self.uploads_dir + "/" + recordFromCache['filename']

            # send file back to client
            if os.path.exists(path):
                return send_from_directory(
                    directory=self.uploads_dir,
                    path=recordFromCache['filename'],
                    as_attachment=True
                )
            else:
                notificationHTML = render_template("notification.html")
                return notificationHTML.replace("INSERT-MESSAGE-HERE","This file reference exists in this database, but it has been deleted from the server..")

    # RE-ROUTE TO HOME PAGE             
    @route('/file', methods=['POST'])
    def createView(self):

        # extract uploaded form contents
        uploadedFile = request.files['file']
        uploadedFileType = request.form["type"]
        bearerToken = request.form['tokenField']
        uploadedFileName = uploadedFile.filename

        # generate paths for file processing
        targetPDFName = uploadedFileName.split(".xlsx")[0] + ".pdf"
        targetPDFPath = "{}/{}".format(
            self.uploads_dir,
            targetPDFName
        )

        # render notification template for dynamic updates
        notificationHTML = render_template("notification.html")

        # Immediately Reject non XLSX Types
        if uploadedFileName.split(".")[-1].lower() != "xlsx":
            return notificationHTML.replace("INSERT-MESSAGE-HERE","Only .xlsx files are supported")
        
        # check if file with same name exists on server, 
        # if so, dynamically calculate unique file name
        elif os.path.exists(targetPDFPath):
            return notificationHTML.replace(
                "INSERT-MESSAGE-HERE",
                "File with path '{}' has already been uploaded, please upload file with unique name.".format(targetPDFPath)
            )

        else:

            # PERFORM CONVERSION TO .PDF HERE & SAVE PDF TO FILESYSTEM
            pdfController.fileConversionDriver(sourceXlsxFile=uploadedFile, targetPDFPath=targetPDFPath, )

            # SAVE REFERENCE INFORMATION TO DATABASE
            # SUPPORTING ONLY ADDING ONE RECORD AT A TIME TO THE SYSTEM
            insertedRecord = dbController.insert_records(
                tableRecord=(
                    (
                        targetPDFName,
                        datetime.datetime.now(),
                        bearerToken,
                        uploadedFileType
                    )
                )
            )

            # provide success message to caller
            return notificationHTML.replace("INSERT-MESSAGE-HERE", """File Successfully Uploaded: {}""".format(json.dumps(insertedRecord, indent=4)))

    # HANDLING 404 ERRORS
    @route('/<path:path>')
    def catch_all(self, path):
        return redirect("/", code=302)


# instantiate PrimaryController FlaskAPI Instance
PrimaryController.register(app, route_base='/')

# trigger invocation of API
if __name__ == '__main__':

    # instantiate flask application
    app.run(host='0.0.0.0', port=5050, debug=True)
    