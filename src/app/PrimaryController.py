import json
import os

# https://pythonbasics.org/flask-upload-file/#:~:text=It%20is%20very%20simple%20to,it%20to%20the%20required%20location.
from werkzeug.utils import secure_filename

# integrate Flask API Class Libraries
from flask import Flask, jsonify, render_template, request
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
                    <td>{}</td>
                </tr>
            """.format(fileRecord["filename"], fileRecord["createdBy"], fileRecord["createdAt"], fileRecord["docType"], fileRecord["uuid"])

        # append table records to HTML Table
        indexHTML = indexHTML.replace("DYNAMIC-TABLE-CONTENT-REPLACED-HERE", tableRecordsHTML)

        # read base-template
        return indexHTML

    # ROUTE #1: FETCH FILE FROM DATABASE BY ID. DISPLAY IN INDEX & RETURN METADATA IN HEADERS (UNIT TEST SUPPORT)
    @route('/file/<name>', methods=['GET'])
    def getTableData(self, name):

        # fetch records from cache
        return jsonify(dbController.return_records_from_cache(name))


    # RE-ROUTE TO HOME PAGE             
    @route('/file', methods=['POST'])
    def createView(self):

        # extract uploaded form contents
        uploadedFile = request.files['file']
        uploadedFileType = request.form["type"]

        # check if file with same name already exists on server, 
        # if so, append "_" to end of file
        if os.path.exists(uploadedFile.filename):
            uploadedFile.filename = uploadedFile.filename + "_"

        # save uploaded file to filesystem
        uploadedFile.save(
            os.path.join(
                self.uploads_dir,
                secure_filename(uploadedFile.filename)
            )
        )
        return 'file uploaded successfully'


# instantiate PrimaryController FlaskAPI Instance
PrimaryController.register(app, route_base='/')

# trigger invocation of API
if __name__ == '__main__':

    # instantiate flask application
    app.run(host='0.0.0.0', port=5050, debug=True)
    