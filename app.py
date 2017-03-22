# @Author: mdrhri-6
# @Date:   2017-03-10T02:36:18+01:00
# @Last modified by:   mdrhri-6
# @Last modified time: 2017-03-22T17:57:05+01:00

from tree_traversal_bottom_up import brb_algorithm
import xlrd
import os
from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

def get_columns_with_node_name():
    data = dict()
    data["Percentage of Loss of cattle"] = "x6"
    data["Social Condition"] = "x7"
    data["Area"] = "x20"
    data["Water Level"] = "x22"
    data["Availability of Cattle Food"] = "x23"
    data["Accomodation"] = "x24"
    data["Availability of Transport"] = "x25"
    data["Length of Road Effected"] = "x26"
    data["Road Damage"] = "x28"
    data["Duration of standing water"] = "x29"
    data["Amount of Crop"] = "x12"
    data["Fertility"] = "x13"
    data["Availability of Labor"] = "x14"
    data["Cost of Raw Materials"] = "x15"
    data["Agricultural Wages"] = "x16"
    data["Financial Condition"] = "x8"
    data["Mental Condition"] = "x9"
    data["Availability of Transport Stuffs"] = "x11"
    data["Cost of Transport"] = "x31"
    data["Frequency of Travellers"] = "x32"
    data["Transportation of Goods"] = "x33"
    data["Transportation Delay"] = "x35"

    data["Directly Intangible"] = "x1"
    data["Directly Tangible"] = "x2"
    data["Indirectly Intangible"] = "x3"
    data["Indirectly Tangible"] = "x4"
    data["Livelihood"] = "x5"
    return data



def get_headings_from_excel():
    # Open excel file
    file_dir = os.path.join(os.getcwd(), 'data_collected_from_bashkhali.xlsx')
    workbook = xlrd.open_workbook(file_dir)
    sh = workbook.sheet_by_index(0)

    # Prepare data from column name
    columns = list()
    row = sh.row(0)
    for i in range(len(row)):
        columns.append(row[i].value)
    return columns

def get_data_from_excel(id):
    # Open excel file
    file_dir = os.path.join(os.getcwd(), 'data_collected_from_bashkhali.xlsx')
    workbook = xlrd.open_workbook(file_dir)
    sh = workbook.sheet_by_index(0)

    if id > 0:
        # Prepare data for a row
        data = list()
        row = sh.row(id)
        for i in range(len(row)):
            data.append(row[i].value)
        return data
    else:
        # Prepare data list from excel.
        # Data Type: list(list)
        data = list()
        for i in range(1, sh.nrows):
            row = sh.row(i)
            row_list = list()
            for k in range(len(row)):
                row_list.append(row[k].value)
            data.append(row_list)
        return data



@app.route('/')
def index():
    # import pdb; pdb.set_trace()
    #data = get_data_from_excel(0)
    data = ""
    #columns = get_headings_from_excel()
    columns = ""
    return render_template('index.html', columns = columns, data=data)

@app.route('/get_row_data/')
def get_row_data():
    id = int(float(request.args.get('id')))
    columns = get_headings_from_excel()[1:]
    data = get_data_from_excel(id)
    structured_data = list()
    column_data = dict()
    str_data = list()
    column_dict = get_columns_with_node_name()
    data = data[1:]
    for each in range(len(data)):
        # print each, columns[each-1], column_dict.get(columns[each-1])
        val = str(data[each])
        if '%' in val:
            val = val.split('%')[0]
            val = str(float(val) / 100)
        column_data[str(column_dict.get(columns[each-1]))] = [columns[each-1], val]
        structured_data.append([column_dict.get(columns[each-1]), columns[each-1], val])

    result = brb_algorithm(structured_data)
    row_data = [str(each) for each in data[1:]]
    return jsonify(columns[1:], row_data, column_data, result)



if __name__ == '__main__':
    app.run()
