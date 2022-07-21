# XLSX To PDF Converter Challenge
Project capable of converting uploaded Excel files to PDF's and seeding results into local database for further processing. Integrated UI technologies to enhance experience and data readability.

## Design/Reference Architecture
2-tier Flask/MySQL application, each hosted as separate containers, orchestrated via docker-compose.
![Reference Architecture Diagram](artifacts/ref-arch.jpg?raw=true "Reference Architecture")

### Technical Notes/Design Considerations
This applications supports conversion of XLSX (tabular data) into PDFs. The UI supports uploading files to server and listing the successfully converted files available for download.
1. **UI/UX:** Since the requirement was primarily focused on file-conversion functionality, I decided to keep frontend as light as possible while preserving desired functionality of uploading & listing files for download. Used Bootstrap 4 for styling page & JQuery to perform filtering on records based on input field contents. 
2. **API:** I selected Python because of its libraries that are perfectly suited for all elements of this job: REST API (Flask), XLSX support (Pandas), Database Connectivity (MySQL Connector), PDF Conversion (FPDF). I wanted to build this solution using Object-Oriented Principles that integrated in all of these libraries.
3. **MySQL:** Since the OpenAPI specification listed a finite-set of DB fields (name, createdDate, createdBy, type) ETC, I decided to implement a relational-database. Also, schema only requires one table to satisfy this required functionalites. **NOTE:** I am storing the files on the system, and staging relative paths & other file data in the DB. Upon file retrieval I'm using the path to programmatically fetch the file from the server.
4. **XLSX -> PDF File Conversion:** Upon .XLSX file upload to server, the .PDF controller uses Pandas to process the excel into to programmatic object for cleansing and manipulation. From there, I adopted and modified a script that works on-top of FPDF to generate dynamic table contents. This library creates flexible table columns based on contents, however, it will only allow cells to grow to a fixed width length, after this point the cells wrap. I programmatically calculate the width of each page my multiplying the number of columns by fixed max of cell length. This ensures we'll never encounter a scenario where the table grows outside the page.
5. **Usage Orchestration:** Docker + Docker Compose allows me the ability to package all dependencies while preserving application functionality and communication between containers.
6. **Edge-Cases & Other Considerations:** This solution cannot handle macros, formulas, image conversion or formatting of cells (text, highlighting, color, background, font, etc). In the application, I wrote logic to reject the upload if the file selected is anything other than .XLSX. I am setting the target filename to preserve the same name of the XLSX file. With that being said, the application rejects the upload if there's a file that already exists on the server with the same name.

## Pre-Req's
### System/Software Installation 
0. MANDATORY: Git
1. MANDATORY: Docker + Docker Compose
2. MANDATORY: Python 3+ (Generating API Hash & Unit-Testing)
3. OPTIONAL: ".sh" Script Interpreter (I.E: git bash)
4. NOTE: If Running Locally, You'll need MySQL installed.


## Getting Started
1. Clone Repo: `git clone https://github.com/Smith-MichaelJ1995/File-Converter-Challenge.git`
2. Ensure Docker Daemon Running.
3. Build + Run Containers: `cd src && sh build-run.sh`
    - *NOTE: The Containers are defaulted to run on ports 5050 (app), 3306 (db). If you have services running on these ports locally, either turn them off OR change port #'s in docker-compose.yml*
4. Instantiate Web-Application (New Terminal, Same Directory): `sh build-run.sh`
    - This script invokes "docker compose build" & "docker compose up"
5. Open browser to localhost:5050 ![Homepage](artifacts/homepage.png?raw=true "Application Homepage")
    - Please test following cases listed below 

## Unit Testing
I've created a series of unit-tests to validate accuracy of XLSX-PDF tabular conversion. Each folder contains a respective xlsx/pdf file. The list below contains links to folder & test-case details. 
1. Basic 5x5 With Numbers & "Lorem Ipsum": 
2. Multiple Sheets, Varying Table Sizes (Multi-Sheet):
3. Table Containing 15 Columns (Max Columns):
4. Table With 15 Words Per Cell (Max Text): 
5. Table Containing Overflowing Rows/Records (Large Data):
6. Chaos Case (Multi-Sheet, Multi-Column, Multi-Words, Overflowing Records):



<!-- 3. Confirm Console Output: ![Unit Test Results](artifacts/unit-tests.png?raw=true "Unit Test Results") -->

## Authors
 - Michael J. Smith

