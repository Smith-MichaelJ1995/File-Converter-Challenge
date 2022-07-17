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

            # perform connection attempt
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
        searchResults = []

        # determine if table exists
        self.myCursor.execute("SELECT * FROM INFORMATION_SCHEMA.TABLES  WHERE TABLE_SCHEMA = '{}' AND TABLE_NAME = '{}';".format(
            os.environ['SQL_DATABASE'],
            tableName
        ))
        tables = self.myCursor.fetchall()

        # only continue processing if we've found results for this table
        if len(tables) > 0:

            # extract all records from table in question
            self.myCursor.execute("SELECT * from {}".format(tableName))
            rows = self.myCursor.fetchall()

            # fetch all records from all rows
            for index, row in enumerate(rows):

                # extract key/value fields
                heroNumber = row[0]
                heroName = row[1]
                heroComics = row[2]
                heroThumbnail = row[3]
                heroDescription = row[4]

                # append search results for future processing
                searchResults.append({
                    "id": heroNumber,
                    "name": heroName,
                    "comics": heroComics,
                    "img": heroThumbnail,
                    "description": heroDescription 
                })

        return searchResults

    # perform operation on class instantiation
    def populate(self):

        # create temporary records placeholder
        records = {}

        # fetch all tables in "intel" database
        self.myCursor.execute("show TABLES;")
        tables = self.myCursor.fetchall()

        # traverse through all tables
        for table in tables:

            # extract column name
            tableName = table[0]
            
            # append item to records container
            records[tableName] = self.extract_records_from_database_table(tableName)
            
        return records

    # given string, remove bad sql characters
    def remove_bad_characters(self, inpt):
        for badChar in self.badChars:
            inpt = inpt.replace(badChar, "")
        return inpt
        
    # return all table names within intel database
    def return_table_names(self):
        return self.records.keys()

    # return table records to viewer
    def return_records_from_cache(self, tableName):
        if tableName in self.records.keys():
            return self.records[tableName]
        else:

            # extract record from database
            databaseRecords = self.extract_records_from_database_table(tableName)

            # only update cache if we've found the specified table data
            if len(databaseRecords) > 0:
                self.records[tableName] = databaseRecords
            
            # return database records to caller
            return databaseRecords
        

    # instantiate expected variables
    def __init__(self):

        # generate DB connection object
        self.myDB = self.connect()

        # generate cursor for inline command invocation
        self.myCursor = self.myDB.cursor()

        # declare list of known bad characters for safety
        self.badChars = ['&','<','>','/','\\','"',"'",'?','+']

        # use selected database
        self.myCursor.execute("USE {};".format(os.environ['SQL_DATABASE']))

        # populate records from database
        self.records = self.populate()

    # insert records into databases specified table
    def insert_records(self, tableName, tableRecords):  
        
        # create table
        cmd = """CREATE TABLE {} (id INTEGER, name VARCHAR(255), comics VARCHAR(1000), image VARCHAR(255), description VARCHAR(1000));""".format(tableName)
        #cmd = """CREATE TABLE spectrum (id INTEGER, name VARCHAR(255), image VARCHAR(255), description VARCHAR(1000));"""
        self.myCursor.execute(cmd)

        # insert records into table
        # DEFINE INSERTION STATEMENT, PROTECT AGAINST SQL INJECTION
        sqlStatement = """INSERT INTO {} (id, name, comics, image, description) VALUES (%s, %s, %s, %s, %s)""".format(tableName)
        
        # invoke statement, add records.
        self.myCursor.executemany(sqlStatement, tableRecords)

        # changes must be commited to the database in order to take effect
        self.myDB.commit()