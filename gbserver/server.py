import random
import copy
from collections import Counter
import urllib.parse
from flask import Flask, jsonify, current_app, request
from flask_cors import CORS
from graphbrain import *
from gbserver.conflicts import conflicts, conflict_topics, conflicts_by_topic
from gbserver.test_data import test_data


app = Flask(__name__)
CORS(app)


@app.route('/api/conflicts/topics')
def conflicts_topics():
    hg = hgraph(current_app.config['HG'])
    table = {'type': 'table',
             'columns': ['id', 'label', 'weight', 'url'],
             'rows': []}
    data = {'viz_blocks': [table]}
    for topic, weight in conflict_topics(hg).most_common():
        url = '/api/conflicts/topic?{}'.format(
            urllib.parse.urlencode({'topic': topic.to_str()}))
        row = {'id': topic.to_str(),
               'label': topic.label(),
               'weight': weight,
               'url': url}
        table['rows'].append(row)
    return jsonify(data)


@app.route('/api/conflicts/all')
def conflicts_all():
    hg = hgraph(current_app.config['HG'])
    graph = {'type': 'graph',
             'layout': 'force-directed',
             'nodes': [],
             'links': []}
    data = {'viz_blocks': [graph]}
    actors = Counter()
    for conflict, weight in conflicts(hg).most_common():
        if weight > 2:
            actor1, actor2 = conflict
            actors[actor1] += 1
            actors[actor2] += 1
            link = {'source': actor1.to_str(),
                    'target': actor2.to_str(),
                    'type': 'conflict',
                    'directed': True,
                    'weight': weight,
                    'label': ''}
            graph['links'].append(link)
    for actor, weight in actors.most_common():
        node = {'id': actor.to_str(),
                'label': actor.label(),
                'faction': 0,
                'weight': weight}
        graph['nodes'].append(node)
    return jsonify(data)


@app.route('/api/conflicts/topic')
def conflicts_topic():
    topic = hedge(request.args.get('topic'))

    graph = {'type': 'graph',
             'layout': 'force-directed',
             'nodes': [],
             'links': []}
    data = {'viz_blocks': [graph]}
    actors = Counter()

    hg = hgraph(current_app.config['HG'])
    for conflict, weight in conflicts_by_topic(hg, topic).most_common():
        actor1, actor2 = conflict
        actors[actor1] += 1
        actors[actor2] += 1
        link = {'source': actor1.to_str(),
                'target': actor2.to_str(),
                'type': 'conflict',
                'directed': True,
                'weight': weight,
                'label': ''}
        graph['links'].append(link)
    for actor, weight in actors.most_common():
        node = {'id': actor.to_str(),
                'label': actor.label(),
                'faction': 0,
                'weight': weight}
        graph['nodes'].append(node)
    return jsonify(data)


@app.route('/api/conflicts1')
def conflicts1():
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
