from create_table_fpdf2 import PDF

# bvalgard example
data = [
    ["First name", "Last name", "Age", "City",], # 'testing','size'],
    ["Jules", "Smith", "34", "San Juan",], # 'testing','size'],
    ["Mary", "Ramos", "45", "Orlando",], # 'testing','size'],
    ["Carlson", "Banks", "19", "Los Angeles",], # 'testing','size'],
    ["Lucas", "Cimon", "31", "Saint-Mahturin-sur-Loire",], # 'testing','size'],
]

pdf = PDF()
pdf.add_page()
pdf.set_font("Times", size=10)

pdf.create_table(table_data = data,title='I\'m the first title', cell_width='even')
pdf.ln()

pdf.output('table_class.pdf')

# WORKING EXAMPLE #1
# data = (
#     ("First name", "Last name", "Age", "City"),
#     ("Jules", "Smith", "34", "San Juan"),
#     ("Mary", "Ramos", "45", "Orlando"),
#     ("Carlson", "Banks", "19", "Los Angeles"),
#     ("Lucas", "Cimon", "31", "Saint-Mahturin-sur-Loire"),
# )

# pdf = FPDF()
# pdf.add_page()
# pdf.set_font("Times", size=10)
# line_height = pdf.font_size * 2.5
# col_width = pdf.epw / 4  # distribute content evenly
# for row in data:
#     for datum in row:
#         pdf.multi_cell(col_width, line_height, datum, border=1,
#                 new_x="RIGHT", new_y="TOP", max_line_height=pdf.font_size)
#     pdf.ln(line_height)
# pdf.output('table_with_cells.pdf')


# WORKING EXAMPLE #2
# TABLE_COL_NAMES = ("First name", "Last name", "Age", "City")
# TABLE_DATA = (
#     ("Jules", "Smith", "34", "San Juan"),
#     ("Mary", "Ramos", "45", "Orlando"),
#     ("Carlson", "Banks", "19", "Los Angeles"),
#     ("Lucas", "Cimon", "31", "Angers"),
# )

# pdf = FPDF()
# pdf.add_page()
# pdf.set_font("Times", size=16)
# line_height = pdf.font_size * 2
# col_width = pdf.epw / 4  # distribute content evenly

# def render_table_header():
#     pdf.set_font(style="B")  # enabling bold text
#     for col_name in TABLE_COL_NAMES:
#         pdf.cell(col_width, line_height, col_name, border=1)
#     pdf.ln(line_height)
#     pdf.set_font(style="")  # disabling bold text

# render_table_header()
# for _ in range(10):  # repeat data rows
#     for row in TABLE_DATA:
#         if pdf.will_page_break(line_height):
#             render_table_header()
#         for datum in row:
#             pdf.cell(col_width, line_height, datum, border=1)
#         pdf.ln(line_height)

# pdf.output("table_with_headers_on_every_page.pdf")



# LOAD USING WORKBOOK

# SET ORIENTATION HANDLE COLUMN SIZES

# USE PDFSAVEOPTIONS TO SAVE IT


# Load Excel file
# workbook = Workbook("julies-transactions-2022.xlsx")

# Convert Excel to PDF
# workbook.save("julies-transactions-2022.pdf", SaveFormat.PDF)

# workbook.close()


# print(df)

# fig, ax =plt.subplots(figsize=(12,4))
# ax.axis('tight')
# ax.axis('off')
# the_table = ax.table(cellText=df.values,colLabels=df.columns,loc='center')

# #https://stackoverflow.com/questions/4042192/reduce-left-and-right-margins-in-matplotlib-plot
# pp = PdfPages("julies-transactions-2022.pdf")
# pp.savefig(fig, bbox_inches='tight')
# pp.close()

# print(xslxFile)

