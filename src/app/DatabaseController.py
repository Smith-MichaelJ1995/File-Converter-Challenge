import mysql.connector
from mysql.connector import errorcode
import os
import json
import time

# instantiate database controller
class DatabaseController:

    # perform connection operation
    def connect(self):

        # keep track of connection attempts
        attemptCount = 0
        connection = None

        # perform 5 total tries, separated by 15 minutes each
        while attemptCount < 5:

            try:

                # perform connection attempt
                connection = mysql.connector.connect(
                    host=os.environ['SQL_HOST'],
                    user=os.environ['SQL_USER'],
                    password=os.environ['SQL_PASSWORD'],  
                    database=os.environ['SQL_DATABASE'],               
                    port=os.environ['SQL_PORT'],
                )

                # connection has been successful
                break

            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                    print("Something is wrong with your user name or password")
                elif err.errno == errorcode.ER_BAD_DB_ERROR:
                    print("Database does not exist")
                else:
                    print("connection = {}".format(connection))
                    print(err)
                
                # increment attempt count, sleep for 15 seconds
                attemptCount += 1
                time.sleep(5)
        
        # determine activity based on connection status
        if connection == None:
            print("QUITTING, FAILED TO CONNECT TO DATABASE")
            exit()
        else:
            print("CONNECTION TO DATABASE SUCCESSFULLY ESTABLISHED")
            return connection

    # generate generic/re-usable function for extracting records from a table
    def extract_records_from_database_table(self, tableName):

        # define search results placeholder
        searchResults = {}

        # determine if table exists
        self.myCursor.execute("SELECT * FROM INFORMATION_SCHEMA.TABLES  WHERE TABLE_SCHEMA = '{}' AND TABLE_NAME = '{}';".format(
            os.environ['SQL_DATABASE'],
            tableName
        ))

        # fetch all records from database
        tables = self.myCursor.fetchall()

        # only continue processing if we've found results for this table
        if len(tables) > 0:

            # extract all records from table in question
            self.myCursor.execute("SELECT * from {}".format(tableName))
            rows = self.myCursor.fetchall()

            # fetch all records from all rows
            for row in rows:

                # extract key/value fields
                uuid = row[0]
                filename = row[1]
                createdAt = row[2]
                createdBy = row[3]
                docType = row[4]

                # append search results for future processing
                searchResults[uuid] = {
                    "uuid": uuid,
                    "filename": filename,
                    "createdAt": createdAt,
                    "createdBy": createdBy,
                    "docType": docType 
                }
        else:
            print("No Records Found For Table, Returning Empty Dataset")

        return searchResults
        
    # return table records to viewer
    # fetch inside database cache, as opposed to querying manually thru all records
    # O(1) lookup, vs manually querying thru each record/key and checking for existance
    def return_record_from_cache(self, uuid):
        try:
            return self.records[int(uuid)]
        except:
            print(uuid in self.records.keys())
            return []

    # return all records from cache
    def return_all_records_from_cache(self):
        return self.records.values()

    # instantiate expected variables
    def __init__(self):

        # generate DB connection object
        self.myDB = self.connect()

        # generate cursor for inline command invocation
        self.myCursor = self.myDB.cursor()

        # set path for reading PDF files, set specific table to use to fetch data
        self.pdfFilePath = "instance/uploads"
        self.tableInScope = "Files"

        # use selected database
        self.myCursor.execute("USE {};".format(os.environ['SQL_DATABASE']))

        # populate records from database
        self.records = self.extract_records_from_database_table(self.tableInScope)

    # insert records into databases specified table
    def insert_records(self, tableRecords):  
        
        # insert records into table
        # DEFINE INSERTION STATEMENT, PROTECT AGAINST SQL INJECTION
        sqlStatement = """INSERT INTO {} (id, name, comics, image, description) VALUES (%s, %s, %s, %s, %s)""".format(self.tableInScope)
        
        # invoke statement, add records.
        self.myCursor.execute(sqlStatement, tableRecords)

        # changes must be commited to the database in order to take effect
        self.myDB.commit()

        # update local cache here database cache here
        self.myCursor.execute("SELECT SCOPE_IDENTITY();")
        insertedID = self.myCursor.fetchall()
        print("InsertedID = {}".format(insertedID))

