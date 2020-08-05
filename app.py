from flask import Flask, request, make_response
from flask_cors import CORS
import csv, os, io
# from werkzeug.wrappers import Response
from werkzeug.exceptions import BadRequest

app = Flask(__name__)
CORS(app, resources=r"/*")

@app.route('/')
def index():
    return '<h1> Hello World </h1>', 200

@app.route('/temp')
def temp():

    return 'Temp data', 200

@app.route('/upload', methods=['POST'])
def getFile():
    try:
        files = request.files['file']
        files.save(files.filename)
        
        return convertFile(files.filename)

        # os.remove(files.filename)

        # # ret_file = open('temp.csv')
        # # data = ret_file.read()
        # si = io.StringIO()
        # csv.writer(si)
        # data = si.getvalue()
        # response = Response(data, mimetype='text/csv')
        # response.headers.set("Content-Disposition", "attachment", filename=files.filename)

        # return response, 200

    except Exception as error:
        print('something went wrong:', error)

        e = BadRequest()
        e.data = {'error': f'Something went wrong: {error}'}
        raise e

        return f'Something went wrong: {error}', 400

def convertFile(filename):
    csv_file = open(filename, 'r')
    csv_reader = csv.reader(csv_file)

    # ret_file = open('temp.csv', 'w+')
    # csv_writer = csv.writer(ret_file)
    si = io.StringIO()
    csv_writer = csv.writer(si)

    i = 0
    for row in csv_reader:
        if i == 0:
            csv_writer.writerow(["Email, First Name, Last Name, Domain"])
            i += 1
        
        try:
            name, domain = row[0].split('@')
            name = name.split('.')

            if len(name) == 1:
                csv_writer.writerow([row[0], name[0], '', domain])
            if len(name) >= 2:
                csv_writer.writerow([row[0], name[0], ''.join(name[1:]), domain])
        except Exception as error:
            csv_writer.writerow([row[0], ''])
        
    csv_file.close()
    os.remove(filename)
    # ret_file.close()
    
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=export.csv"
    output.headers["Content-type"] = "text/csv"
    
    return output

if __name__ == '__main__':
    app.run(debug=True)

#https://stackoverflow.com/questions/26997679/writing-a-csv-from-flask-framework
#https://stackoverflow.com/questions/28011341/create-and-download-a-csv-file-from-a-flask-view
