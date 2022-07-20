from create_table_fpdf2 import PDF
import pandas as pd

# given dimension key return expected
def determine_expected_dimensions(dimensionKey):

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

# fetch excel file from filesystem
xlsxFileName = "Julie-Transactions-2022.xlsx"
xlsxFile = pd.ExcelFile(xlsxFileName)
xlsxSheetNames = xlsxFile.sheet_names

# instantiate PDF object/instance
pdf = PDF("L", "mm")
pdf.set_font("Times", size=10)

# iterate through all sheets in file
for sheet_name in xlsxSheetNames:

    # fetch excel from filesystem
    df = pd.read_excel(xlsxFileName, sheet_name=sheet_name)
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
        pdf.add_page("L", determine_expected_dimensions(dimensionKey))

    # determine total character count of column names in header
    for row in tableHeaderRow:
        tableHeaderStringLenCount += len(row)

    # generate PDF table within record
    pdf.create_table(table_data = tableRecords, cell_width='uneven')
    pdf.ln()

# save to filesystem
pdf.output('Julie-Transactions-2022.pdf')







