from flask import Flask, jsonify
import subprocess
import json
import os

app = Flask(__name__)

@app.route('/run-nuxeo-monitor', methods=['GET'])
def run_monitor():

    try:
        subprocess.run(
            ['python', 'main.py'],
            check=True
        )

        if os.path.exists('results.json'):

            with open('results.json', 'r') as f:
                results = json.load(f)

            return jsonify({
                'status': 'success',
                'results': results
            })

        return jsonify({
            'status': 'completed',
            'message': 'No results file found'
        })

    except Exception as e:

        return jsonify({
            'status': 'error',
            'message': str(e)
        })

@app.route('/')
def home():
    return 'Nuxeo Monitor API Running'

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=5000
    )