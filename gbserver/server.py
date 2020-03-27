from collections import Counter
import urllib.parse
from flask import Flask, jsonify, current_app, request
from flask_cors import CORS
from graphbrain import *
from gbserver.actors import actor_info
from gbserver.conflicts import conflict_topics, conflicts_by_topic
from gbserver.factions import Factions


app = Flask(__name__)
CORS(app)


def topic_url(topic):
    return '/api/conflicts/topic?{}'.format(
        urllib.parse.urlencode({'topic': topic.to_str()}))


@app.route('/api/conflicts/topics')
def conflicts_topics():
    hg = hgraph(current_app.config['HG'])
    table = {'type': 'table',
             'columns': ['id', 'label', 'weight', 'url'],
             'rows': []}
    data = {'viz_blocks': [table]}
    for topic, weight in conflict_topics(hg).most_common():
        url = topic_url(topic),
        row = {'id': topic.to_str(),
               'label': topic.label(),
               'weight': weight,
               'url': url}
        table['rows'].append(row)
    return jsonify(data)


@app.route('/api/conflicts/topic')
def conflicts_topic():
    topic = hedge(request.args.get('topic'))

    graph = {'type': 'graph',
             'layout': 'force-directed',
             'topic_label': topic.label(),
             'nodes': [],
             'links': []}
    data = {'viz_blocks': [graph]}
    actors = Counter()

    hg = hgraph(current_app.config['HG'])
    conflict_pairs = []
    conflicts = conflicts_by_topic(hg, topic)
    for conflict in conflicts:
        conflict_pairs.append(conflict)
        actor1, actor2 = conflict
        actors[actor1] += 1
        actors[actor2] += 1
        conflicts_data = conflicts[conflict]
        weight = len(conflicts_data)
        headlines = [conflict_data['text'] for conflict_data in conflicts_data
                     if conflict_data['text'] is not None]
        other_topics = set()
        for conflict_data in conflicts_data:
            for topic in conflict_data['other_topics']:
                other_topics.add(topic)

        other_topics = [{'label': t.label(),
                         'url': topic_url(t)} for t in other_topics]

        info = {'headlines': headlines,
                'other_topics': list(other_topics)}

        link = {'source': actor1.to_str(),
                'target': actor2.to_str(),
                'type': 'conflict',
                'directed': True,
                'weight': weight,
                'label': '',
                'info': info}
        graph['links'].append(link)

    factions = Factions(conflict_pairs)

    for actor, weight in actors.most_common():
        node = {'id': actor.to_str(),
                'label': actor.label(),
                'faction': 0,
                'weight': weight,
                'faction': factions.faction(actor),
                'info': actor_info(hg, actor)}
        graph['nodes'].append(node)
    return jsonify(data)
