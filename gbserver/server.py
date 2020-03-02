import random
import copy
from flask import Flask, jsonify, current_app
from flask_cors import CORS
from gbserver.test_data import test_data


app = Flask(__name__)
CORS(app)


@app.route('/api/conflicts1')
def conflicts1():
    print(current_app.config['HG'])
    return jsonify(test_data)


@app.route('/api/conflicts2')
def conflicts2():
    random.seed(36)
    data = copy.deepcopy(test_data)
    data['viz_blocks'][0]['layout'] = 'predefined'
    for node in data['viz_blocks'][0]['nodes']:
        node['x'] = random.random()
        node['y'] = random.random()
    return jsonify(data)
