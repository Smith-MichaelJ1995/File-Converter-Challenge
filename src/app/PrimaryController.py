# import hashlib
# import requests
import json
import os
from tkinter import *

# integrate Flask API Class Libraries
from flask import Flask, jsonify, redirect, render_template, request
from flask_classful import FlaskView, route

# integrate Database & MarvelController class controller
from DatabaseController import DatabaseController

# Instantiate Supporting Classes
dbController = DatabaseController()

# instantiate app instance
app = Flask(__name__)

# Controller Class To Integrate with UI, MarvelAPI Backend, Local Database.
class PrimaryController(FlaskView):

    # ROUTE #0: DISPLAY ALL TABLES (CHARACTERS) IN DATABASE AS CLICKABLE LINKS
    @route('/', methods=["GET"])
    def index(self):
        print("READING FROM INDEX FILE")
        return render_template("index.html")


    # ROUTE #1: FETCH FILE FROM DATABASE BY ID. DISPLAY IN INDEX & RETURN METADATA IN HEADERS (UNIT TEST SUPPORT)
    @route('/file/<name>', methods=['GET'])
    def getTableData(self, name):

        # fetch records from cache
        return jsonify(dbController.return_records_from_cache(name))


    # RE-ROUTE TO HOME PAGE             
    @route('/file', methods=['PUT'])
    def createView(self):

        print("HELLO FROM FILE PUT FUNCTION!!!!!")
        print(request.data)
        
     
        # RE-ROUTE TO VIEW PAGE 
        # character already exists, return back existing page
        return "{}".format(request.data)


# instantiate PrimaryController FlaskAPI Instance
PrimaryController.register(app, route_base='/')

# trigger invocation of API
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050, debug=True)
    #instantiate neighboring controller classes
    