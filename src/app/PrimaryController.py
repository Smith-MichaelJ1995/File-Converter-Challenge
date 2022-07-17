# import hashlib
# import requests
import json
import os
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

        # read base-template
        return render_template("index.html")

    # ROUTE #1: FETCH FILE FROM DATABASE BY ID. DISPLAY IN INDEX & RETURN METADATA IN HEADERS (UNIT TEST SUPPORT)
    @route('/file/<name>', methods=['GET'])
    def getTableData(self, name):

        # fetch records from cache
        return jsonify(dbController.return_records_from_cache(name))


    # RE-ROUTE TO HOME PAGE             
    @route('/file', methods=['POST'])
    def createView(self):

        f = request.files['file']
        f.save(
            os.path.join(
                self.uploads_dir,
                secure_filename(f.filename)
            )
        )
        return 'file uploaded successfully'


# instantiate PrimaryController FlaskAPI Instance
PrimaryController.register(app, route_base='/')

# trigger invocation of API
if __name__ == '__main__':

    # instantiate flask application
    app.run(host='0.0.0.0', port=5050, debug=True)
    