import json
import os

# https://pythonbasics.org/flask-upload-file/#:~:text=It%20is%20very%20simple%20to,it%20to%20the%20required%20location.
from werkzeug.utils import secure_filename

# integrate Flask API Class Libraries
from flask import Flask, jsonify, render_template, request, send_from_directory
from flask_classful import FlaskView, route

# integrate Database & MarvelController class controller
from DatabaseController import DatabaseController

# Instantiate Supporting Classes
dbController = DatabaseController()

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

        # send file back to client
        return send_from_directory(
            directory=self.uploads_dir,
            path=recordFromCache['filename'],
            as_attachment=True
        )


    # RE-ROUTE TO HOME PAGE             
    @route('/file', methods=['POST'])
    def createView(self):

        # extract uploaded form contents
        uploadedFile = request.files['file']
        uploadedFileType = request.form["type"]
        bearerToken = request.form['tokenField']
        fileName = uploadedFile.filename
        path = "{}/{}".format(self.uploads_dir, fileName)

        print("REQUIRED VARIABLES: ")
        print(uploadedFile, uploadedFileType, bearerToken, fileName, path)

        # check if file with same name already exists on server, 
        # if so, append "_" to end of file
        if os.path.exists(path):

            # placeholder for extra file count
            fileExistanceCount = 1

            # work to create new file name
            while os.path.exists(path):

                # if conflicting file, rename with random integer appended onto end of it
                fileName = fileName.replace(".pdf", "-{}.pdf".format(fileExistanceCount))

                # update file path
                path = "{}/{}".format(self.uploads_dir, fileName)

                # increment file existance count for next conflict
                fileExistanceCount += 1
            

        # save uploaded XLSX file to filesystem
        uploadedFile.save(
            os.path.join(
                "instance/uploads",
                secure_filename(fileName)
            )
        )

        # PERFORM CONVERSION TO .PDF HERE

        # SAVE PDF TO FILESYSTEM

        # SAVE METADATA TO DATABASE
        return 'file uploaded successfully'


# instantiate PrimaryController FlaskAPI Instance
PrimaryController.register(app, route_base='/')

# trigger invocation of API
if __name__ == '__main__':

    # instantiate flask application
    app.run(host='0.0.0.0', port=5050, debug=True)
    