from flask import Flask, jsonify
from main import run_monitor

app = Flask(__name__)

@app.route('/')

def home():

    return "Nuxeo Monitor API Running"

@app.route('/run-nuxeo-monitor')

def monitor():

    result = run_monitor()

    return jsonify(result)

if __name__ == '__main__':

    app.run(
        host='0.0.0.0',
        port=8080
    )