# THIS WAS ORIGIONALLY CREATED BY https://github.com/bvalgard/create-pdf-with-python-fpdf2
# I UPDATED FILE TO REMOVE NON-REQUIRED FUNCTIONALITIES, SUPPORT TEXT WRAPPING, AND CLEAR COMMENTATION
from fpdf import FPDF
from PDFTableGenerator import PDFTableGenerator
import pandas as pd

class PDFController(FPDF):

    # generate PDFTableGenerator instance for controller
    def __init__(self) -> None:
        pass
        #self.pdfTableGenerator = PDFTableGenerator()

    # given dimension key return expected
    def determine_expected_dimensions(self, dimensionKey):

        # determine placeholder for computed dimensions
        computedDimensions = ()

        # smallest case
        if dimensionKey < 500:
            computedDimensions = (175, 225)
        elif dimensionKey >= 500 and dimensionKey < 625:
            computedDimensions = (225, 275)
        elif dimensionKey >= 625 and dimensionKey < 750:
            computedDimensions = (275, 325)
        elif dimensionKey >= 750 and dimensionKey < 875:
            computedDimensions = (325, 375)
        elif dimensionKey >= 875 and dimensionKey < 1000:
            computedDimensions = (375, 425)
        else:
            computedDimensions = (425, 475)

        # display + return computed dimensions to caller
        #print("Computed Dimensions = {}".format(computedDimensions))
        return computedDimensions

    # given provided file name, drive conversion from XLSX to PDF
    def fileConversionDriver(self, sourceXlsxFile, targetPDFPath):

        # fetch excel file from filesystem
        xlsxFile = pd.ExcelFile(sourceXlsxFile, engine='openpyxl')
        pdfFileName = targetPDFPath.split(".")[0] + ".pdf"
        xlsxSheetNames = xlsxFile.sheet_names

        # instantiate PDF object/instance
        pdf = PDFTableGenerator("L", "mm")
        pdf.set_font("Times", size=10)

        # iterate through all sheets in file
        for sheet_name in xlsxSheetNames:

            # fetch excel from filesystem
            df = pd.read_excel(sourceXlsxFile, sheet_name=sheet_name)
            df = df.fillna(value="")
            df = df.astype(str)

            # compute records to be inserted into xlsx
            tableHeaderRow = list(df.columns.values)
            tableHeaderStringLenCount = 0
            tableRecords = df.values.tolist()
            tableRecords.insert(0, tableHeaderRow)

            # calculate expected dimension key (total # of characters * total # of columns)
            dimensionKey = tableHeaderStringLenCount * len(tableHeaderRow)

            # dynamically build page format based on table sizing
            if dimensionKey <= 700:
                pdf.add_page("L")
            else:
                # stretch page to max width
                pdf.add_page("L", self.determine_expected_dimensions(dimensionKey))

            # determine total character count of column names in header
            for row in tableHeaderRow:
                tableHeaderStringLenCount += len(row)

            # generate PDF table within record
            pdf.create_table(table_data = tableRecords, cell_width='uneven')
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


    