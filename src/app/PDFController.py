# THIS WAS ORIGIONALLY CREATED BY https://github.com/bvalgard/create-pdf-with-python-fpdf2
# I UPDATED FILE TO REMOVE NON-REQUIRED FUNCTIONALITIES, SUPPORT TEXT WRAPPING, AND CLEAR COMMENTATION
from fpdf import FPDF
from PDFTableGenerator import PDFTableGenerator
import pandas as pd

class PDFController(FPDF):

    # generate PDFTableGenerator instance for controller
    def __init__(self) -> None:
        # instantiate max line/column length
        self.maxColumnLength = 75

    # given provided file name, drive conversion from XLSX to PDF
    def fileConversionDriver(self, sourceXlsxFile, targetPDFPath):

        # fetch excel file from filesystem
        xlsxFile = pd.read_excel(sourceXlsxFile, engine='openpyxl', sheet_name=None)
        pdfFileName = targetPDFPath.split(".")[0] + ".pdf"
        xlsxSheetNames = xlsxFile.keys()

        # instantiate PDF object/instance
        pdf = PDFTableGenerator("L", "mm")
        pdf.set_font("Times", size=10)

        # iterate through all sheets in file
        for sheet_name in xlsxSheetNames:

            # fetch excel from filesystem
            df = xlsxFile[sheet_name]
            df = df.fillna(value="")
            df = df.astype(str)

            # compute records to be inserted into xlsx
            tableHeaderRow = list(df.columns.values)
            tableRecords = df.values.tolist()
            tableRecords.insert(0, tableHeaderRow)
            tableHeaderCount = len(tableHeaderRow)

            # calculate maximum possible page width (total # of characters * total # of columns)
            dimensionKey = tableHeaderCount * self.maxColumnLength

            # dynamically build page format based on table sizing
            pdf.add_page("L", (dimensionKey+25, dimensionKey+50))

            # generate PDF table within record
            pdf.create_table(table_data = tableRecords, title="Table: {}".format(sheet_name), maxColumnLength=self.maxColumnLength)
            pdf.ln()

        # save newly created PDF to filesystem
        try:

            # write file to system
            pdf.output(targetPDFPath)

            # return newly created file name to PrimaryController
            return pdfFileName
        
        except Exception as e:

            # print error message and return None to caller
            print(e)
            
            return None


    