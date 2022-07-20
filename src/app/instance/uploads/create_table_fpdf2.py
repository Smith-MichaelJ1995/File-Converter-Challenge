# THIS WAS ORIGIONALLY CREATED BY https://github.com/bvalgard/create-pdf-with-python-fpdf2
# I UPDATED FILE TO REMOVE NON-REQUIRED FUNCTIONALITIES, SUPPORT TEXT WRAPPING, AND CLEAR COMMENTATION

from fpdf import FPDF

class PDF(FPDF):
    def create_table(self, table_data, title='', data_size = 10, title_size=12, align_data='L', align_header='L', cell_width='even', x_start='x_default',emphasize_data=[], emphasize_style=None,emphasize_color=(0,0,0)): 
        """
        table_data: 
                    list of lists with first element being list of headers
        title: 
                    (Optional) title of table (optional)
        data_size: 
                    the font size of table data
        title_size: 
                    the font size fo the title of the table
        align_data: 
                    align table data
                    L = left align
                    C = center align
                    R = right align
        align_header: 
                    align table data
                    L = left align
                    C = center align
                    R = right align
        cell_width: 
                    even: evenly distribute cell/column width
                    uneven: base cell size on lenght of cell/column items
                    int: int value for width of each cell/column
                    list of ints: list equal to number of columns with the widht of each cell / column
        x_start: 
                    where the left edge of table should start
        emphasize_data:  
                    which data elements are to be emphasized - pass as list 
                    emphasize_style: the font style you want emphaized data to take
                    emphasize_color: emphasize color (if other than black) 
        
        """

        # instantiate max line/column length
        maxLength = 100

        # Get Maximum Width of Every Column
        def get_col_widths():
            
            # placehold longest column f/e row
            col_widths = []

            # searching through columns for largest sized cell (not rows but cols)
            for col in range(len(table_data[0])): # for every row
                longest = 0 
                for row in range(len(table_data)):

                    # extract cell content and text length
                    cell_value = str(table_data[row][col])
                    value_length = self.get_string_width(cell_value)

                    # set maximum length for each column, enable wrapping
                    if value_length > longest and value_length < maxLength:
                        longest = value_length
                    elif value_length > longest and value_length > maxLength:
                        longest = maxLength

                # stage column values for table
                col_widths.append(longest + 2) # add 2 for padding

            return col_widths
            
        # extracting header/row data
        header = table_data[0]
        data = table_data[1:]
        
        # set file properties
        line_height = self.font_size * 2.5

        # fetch column widths from helper function
        col_width = get_col_widths()

        # print(col_width)
        #exit()

        # set font size
        self.set_font(size=data_size)

        # apply header row onto table
        y1 = self.get_y()
        x_left = self.get_x()
        x_right = self.epw + x_left

        # INSERT HEADER DATA INTO TABLE
        for i in range(len(header)):
            datum = header[i]
            self.multi_cell(col_width[i], line_height, datum, border=0, align=align_header, ln=3, max_line_height=self.font_size)
            x_right = self.get_x()

        # move cursor back to the left margin
        # computing required line height value
        self.ln(line_height) 
        y2 = self.get_y()

        # write top & bottom lines
        self.line(x_left,y1,x_right,y1)
        self.line(x_left,y2,x_right,y2)


        # INSERT CONTENT/DATA INTO TABLE
        for i in range(len(data)):
            # fetch row data from table
            row = data[i]
            for i in range(len(row)):

                # fetch data from cell
                datum = row[i]

                # this will only work if cell type is string
                if not isinstance(datum, str):
                    datum = str(datum)

                # fetch column width
                adjusted_col_width =  col_width[i] 

                # create cell instance with formatting, fonts, and desired width
                self.multi_cell(adjusted_col_width, line_height, datum, border=0, align=align_data, ln=3, max_line_height=self.font_size) # ln = 3 - move cursor to right with same vertical offset # this uses an object named self

            self.ln(line_height) # move cursor back to the left margin
        
        # get measurements for bottom line in table
        y3 = self.get_y()

        # write bottom line onto table
        self.line(x_left,y3,x_right,y3)