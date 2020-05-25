from flask import Flask, send_file, request, jsonify
import requests, csv

app = Flask(__name__)

querystring = {"format":"json"}
headers = {
    'x-rapidapi-host': "ip-geo-location.p.rapidapi.com",
    'x-rapidapi-key': "87f71c1fd8msh4e2d71d5b8630ecp1a9b4fjsn97510659cad7"
    }

@app.route('/')
def index():
    url = "https://ip-geo-location.p.rapidapi.com/ip/" + request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    response = requests.request("GET", url, headers=headers, params=querystring)
    filename = 'pixel.gif'
    log(response.json())
    return send_file(filename, 'image/gif')

def log(response):
    data = {}
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
    with open(r'log.csv', 'a', newline='') as csvfile:
        fieldnames = ['IP Address', 'City', 'State', 'Country', 'Pin Code', 'Coordinates', 'ISP']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow(data)

if __name__ == "__main__":
    app.run()
