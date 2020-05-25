from flask import Flask, send_file, request, jsonify, render_template
import requests, csv
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)

querystring = {"format":"json"}
headers = {
    'x-rapidapi-host': "ip-geo-location.p.rapidapi.com",
    'x-rapidapi-key': "87f71c1fd8msh4e2d71d5b8630ecp1a9b4fjsn97510659cad7"
    }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/receipt')
def receipt():
    url = "https://ip-geo-location.p.rapidapi.com/ip/" + fetch_ip()
    response = requests.request("GET", url, headers=headers, params=querystring)
    filename = 'pixel.gif'
    log(response.json(), request.args.get('id'))
    return send_file(filename, 'image/gif')

@app.route('/view')
def view():
    output = []
    if not request.headers.getlist("X-Forwarded-For"):
       ip = request.remote_addr
    else:
       ip = request.headers.getlist("X-Forwarded-For")[0]
    try:
        with open(r'log.csv', 'r', newline = '') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                output.append(row)
    except:
        output.append("--------")
    return render_template('view.html', output = output, ip = fetch_ip())

def fetch_ip():
    if not request.headers.getlist("X-Forwarded-For"):
       return request.remote_addr
    else:
       return request.headers.getlist("X-Forwarded-For")[0]

def log(response, uid = 'Null'):
    data = {}
    data['ID'] = uid
    data['IP Address'] = response['ip']
    data['City'] = response['city']['name']
    data['State'] = response['area']['name']
    data['Country'] = response['country']['name']
    data['Pin Code'] =  response['postcode']
    try:
        data['Coordinates'] = str(response['location']['latitude']) + 'N ' + str(response['location']['longitude']) + 'E'
    except:
        data['Coordinates'] = 'Not Found'
    data['ISP'] = response['asn']['organisation']
    with open(r'log.csv', 'a', newline = '') as csvfile:
        fieldnames = ['ID','IP Address', 'City', 'State', 'Country', 'Pin Code', 'Coordinates', 'ISP']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow(data)

if __name__ == "__main__":
    app.run()
