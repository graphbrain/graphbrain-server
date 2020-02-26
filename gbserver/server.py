import random
import copy
from flask import Flask, jsonify
from flask_cors import CORS


test_data = {
    "graph": {"layout": "force-directed"},
    "nodes": [
        {
            "id": "(+/b.am/. president/cp.s/en trump/cp.s/en)",
            "label": "president trump",
            "faction": 2,
            "weight": 2
        },
        {
            "id": "rubio/cp.s/en",
            "label": "rubio",
            "faction": 0,
            "weight": 4
        },
        {
            "id": "(+/b.am/. ted/cp.s/en cruz/cp.s/en)",
            "label": "ted cruz",
            "faction": 2,
            "weight": 6
        },
        {
            "id": "mcconnell/cp.s/en",
            "label": "mcconnell",
            "faction": 0,
            "weight": 6
        },
        {
            "id": "(+/b.am/. white/cp.s/en house/cp.s/en)",
            "label": "white house",
            "faction": 2,
            "weight": 10
        },
        {
            "id": "(+/b.am/. scott/cp.s/en walker/cp.s/en)",
            "label": "scott walker",
            "faction": 2,
            "weight": 3
        },
        {
            "id": "gop/cp.s/en",
            "label": "gop",
            "faction": 0,
            "weight": 26
        },
        {
            "id": "boehner/cp.s/en",
            "label": "boehner",
            "faction": 2,
            "weight": 6
        },
        {
            "id": "(+/b.am/. rand/cp.s/en paul/cp.s/en)",
            "label": "rand paul",
            "faction": 1,
            "weight": 4
        },
        {
            "id": "democrats/cp.p/en",
            "label": "democrats",
            "faction": 0,
            "weight": 23
        },
        {
            "id": "trump/cp.s/en",
            "label": "trump",
            "faction": 2,
            "weight": 130
        },
        {
            "id": "republicans/cp.p/en",
            "label": "republicans",
            "faction": 0,
            "weight": 30
        },
        {
            "id": "mccain/cp.s/en",
            "label": "mccain",
            "faction": 1,
            "weight": 13
        },
        {
            "id": "spicer/cp.s/en",
            "label": "spicer",
            "faction": 2,
            "weight": 2
        },
        {
            "id": "(+/b.am/. elizabeth/cp.s/en warren/cp.s/en)",
            "label": "elizabeth warren",
            "faction": 0,
            "weight": 9
        },
        {
            "id": "christie/cp.s/en",
            "label": "christie",
            "faction": 2,
            "weight": 3
        },
        {
            "id": "biden/cp.s/en",
            "label": "biden",
            "faction": 0,
            "weight": 3
        },
        {
            "id": "u_s_/cp.s/en",
            "label": "u s ",
            "faction": 0,
            "weight": 4
        },
        {
            "id": "(+/b.am/. jeb/cp.s/en bush/cp.s/en)",
            "label": "jeb bush",
            "faction": 0,
            "weight": 5
        },
        {
            "id": "obama/cp.s/en",
            "label": "obama",
            "faction": 1,
            "weight": 118
        },
        {
            "id": "clinton/cp.s/en",
            "label": "clinton",
            "faction": 0,
            "weight": 30
        },
        {
            "id": "(+/b.am/. bernie/cp.s/en sanders/cp.s/en)",
            "label": "bernie sanders",
            "faction": 1,
            "weight": 8
        },
        {
            "id": "russia/cp.s/en",
            "label": "russia",
            "faction": 0,
            "weight": 11
        },
        {
            "id": "(+/b.am/. president/cp.s/en obama/cp.s/en)",
            "label": "president obama",
            "faction": 1,
            "weight": 3
        }
    ],
    "links": [
        {
            "origin": "(+/b.am/. bernie/cp.s/en sanders/cp.s/en)",
            "target": "(+/b.am/. ted/cp.s/en cruz/cp.s/en)",
            "type": "conflict",
            "directed": True,
            "weight": 1,
            "label": "Süddeutsche Zeitung"
        },
        {
            "origin": "(+/b.am/. bernie/cp.s/en sanders/cp.s/en)",
            "target": "clinton/cp.s/en",
            "type": "conflict",
            "directed": True,
            "weight": 1,
            "label": "Süddeutsche Zeitung"
        },
        {
            "origin": "(+/b.am/. bernie/cp.s/en sanders/cp.s/en)",
            "target": "democrats/cp.p/en",
            "type": "conflict",
            "directed": True,
            "weight": 1,
            "label": "The Guardian"
        },
        {
            "origin": "(+/b.am/. bernie/cp.s/en sanders/cp.s/en)",
            "target": "gop/cp.s/en",
            "type": "conflict",
            "directed": True,
            "weight": 2,
            "label": "Süddeutsche Zeitung"
        },
        {
            "origin": "(+/b.am/. bernie/cp.s/en sanders/cp.s/en)",
            "target": "trump/cp.s/en",
            "type": "conflict",
            "directed": True,
            "weight": 3,
            "label": "Le Monde"
        },
        {
            "origin": "(+/b.am/. bernie/cp.s/en sanders/cp.s/en)",
            "target": "trump/cp.s/en",
            "type": "conflict",
            "directed": True,
            "weight": 2,
            "label": "The Guardian"
        },
        {
            "origin": "(+/b.am/. elizabeth/cp.s/en warren/cp.s/en)",
            "target": "(+/b.am/. white/cp.s/en house/cp.s/en)",
            "type": "conflict",
            "directed": True,
            "weight": 1,
            "label": "Le Monde"
        },
        {
            "origin": "(+/b.am/. elizabeth/cp.s/en warren/cp.s/en)",
            "target": "democrats/cp.p/en",
            "type": "conflict",
            "directed": True,
            "weight": 1,
            "label": "The Guardian"
        },
        {
            "origin": "(+/b.am/. elizabeth/cp.s/en warren/cp.s/en)",
            "target": "gop/cp.s/en",
            "type": "conflict",
            "directed": True,
            "weight": 2,
            "label": "New York Times"
        },
        {
            "origin": "(+/b.am/. elizabeth/cp.s/en warren/cp.s/en)",
            "target": "obama/cp.s/en",
            "type": "conflict",
            "directed": True,
            "weight": 1,
            "label": "Washington Post"
        },
        {
            "origin": "(+/b.am/. elizabeth/cp.s/en warren/cp.s/en)",
            "target": "republicans/cp.p/en",
            "type": "conflict",
            "directed": True,
            "weight": 1,
            "label": "The Guardian"
        },
        {
            "origin": "(+/b.am/. elizabeth/cp.s/en warren/cp.s/en)",
            "target": "trump/cp.s/en",
            "type": "conflict",
            "directed": True,
            "weight": 2,
            "label": "Süddeutsche Zeitung"
        },
        {
            "origin": "(+/b.am/. jeb/cp.s/en bush/cp.s/en)",
            "target": "obama/cp.s/en",
            "type": "conflict",
            "directed": True,
            "weight": 2,
            "label": "Washington Post"
        },
        {
            "origin": "(+/b.am/. jeb/cp.s/en bush/cp.s/en)",
            "target": "trump/cp.s/en",
            "type": "conflict",
            "directed": True,
            "weight": 1,
            "label": "Washington Post"
        },
        {
            "origin": "(+/b.am/. president/cp.s/en obama/cp.s/en)",
            "target": "republicans/cp.p/en",
            "type": "conflict",
            "directed": True,
            "weight": 2,
            "label": "The Guardian"
        },
        {
            "origin": "(+/b.am/. president/cp.s/en trump/cp.s/en)",
            "target": "obama/cp.s/en",
            "type": "conflict",
            "directed": True,
            "weight": 1,
            "label": "New York Times"
        },
        {
            "origin": "(+/b.am/. president/cp.s/en trump/cp.s/en)",
            "target": "republicans/cp.p/en",
            "type": "conflict",
            "directed": True,
            "weight": 1,
            "label": "The Guardian"
        },
        {
            "origin": "(+/b.am/. rand/cp.s/en paul/cp.s/en)",
            "target": "(+/b.am/. jeb/cp.s/en bush/cp.s/en)",
            "type": "conflict",
            "directed": True,
            "weight": 1,
            "label": "Süddeutsche Zeitung"
        },
        {
            "origin": "(+/b.am/. rand/cp.s/en paul/cp.s/en)",
            "target": "(+/b.am/. ted/cp.s/en cruz/cp.s/en)",
            "type": "conflict",
            "directed": True,
            "weight": 1,
            "label": "The Guardian"
        },
        {
            "origin": "(+/b.am/. rand/cp.s/en paul/cp.s/en)",
            "target": "gop/cp.s/en",
            "type": "conflict",
            "directed": True,
            "weight": 1,
            "label": "New York Times"
        },
        {
            "origin": "(+/b.am/. scott/cp.s/en walker/cp.s/en)",
            "target": "obama/cp.s/en",
            "type": "conflict",
            "directed": True,
            "weight": 1,
            "label": "Süddeutsche Zeitung"
        },
        {
            "origin": "(+/b.am/. ted/cp.s/en cruz/cp.s/en)",
            "target": "(+/b.am/. president/cp.s/en obama/cp.s/en)",
            "type": "conflict",
            "directed": True,
            "weight": 1,
            "label": "Le Monde"
        },
        {
            "origin": "(+/b.am/. ted/cp.s/en cruz/cp.s/en)",
            "target": "democrats/cp.p/en",
            "type": "conflict",
            "directed": True,
            "weight": 2,
            "label": "Le Monde"
        },
        {
            "origin": "(+/b.am/. white/cp.s/en house/cp.s/en)",
            "target": "gop/cp.s/en",
            "type": "conflict",
            "directed": True,
            "weight": 2,
            "label": "The Guardian"
        },
        {
            "origin": "(+/b.am/. white/cp.s/en house/cp.s/en)",
            "target": "obama/cp.s/en",
            "type": "conflict",
            "directed": True,
            "weight": 2,
            "label": "Washington Post"
        },
        {
            "origin": "(+/b.am/. white/cp.s/en house/cp.s/en)",
            "target": "republicans/cp.p/en",
            "type": "conflict",
            "directed": True,
            "weight": 3,
            "label": "Süddeutsche Zeitung"
        },
        {
            "origin": "(+/b.am/. white/cp.s/en house/cp.s/en)",
            "target": "russia/cp.s/en",
            "type": "conflict",
            "directed": True,
            "weight": 1,
            "label": "Washington Post"
        },
        {
            "origin": "biden/cp.s/en",
            "target": "clinton/cp.s/en",
            "type": "conflict",
            "directed": True,
            "weight": 1,
            "label": "The Guardian"
        },
        {
            "origin": "biden/cp.s/en",
            "target": "democrats/cp.p/en",
            "type": "conflict",
            "directed": True,
            "weight": 1,
            "label": "Süddeutsche Zeitung"
        },
        {
            "origin": "biden/cp.s/en",
            "target": "gop/cp.s/en",
            "type": "conflict",
            "directed": True,
            "weight": 1,
            "label": "Süddeutsche Zeitung"
        },
        {
            "origin": "boehner/cp.s/en",
            "target": "obama/cp.s/en",
            "type": "conflict",
            "directed": True,
            "weight": 5,
            "label": "New York Times"
        },
        {
            "origin": "boehner/cp.s/en",
            "target": "obama/cp.s/en",
            "type": "conflict",
            "directed": True,
            "weight": 3,
            "label": "Washington Post"
        },
        {
            "origin": "christie/cp.s/en",
            "target": "(+/b.am/. rand/cp.s/en paul/cp.s/en)",
            "type": "conflict",
            "directed": True,
            "weight": 1,
            "label": "The Guardian"
        },
        {
            "origin": "christie/cp.s/en",
            "target": "obama/cp.s/en",
            "type": "conflict",
            "directed": True,
            "weight": 2,
            "label": "New York Times"
        },
        {
            "origin": "clinton/cp.s/en",
            "target": "obama/cp.s/en",
            "type": "conflict",
            "directed": True,
            "weight": 2,
            "label": "New York Times"
        },
        {
            "origin": "clinton/cp.s/en",
            "target": "republicans/cp.p/en",
            "type": "conflict",
            "directed": True,
            "weight": 1,
            "label": "New York Times"
        },
        {
            "origin": "clinton/cp.s/en",
            "target": "trump/cp.s/en",
            "type": "conflict",
            "directed": True,
            "weight": 10,
            "label": "Süddeutsche Zeitung"
        },
        {
            "origin": "clinton/cp.s/en",
            "target": "trump/cp.s/en",
            "type": "conflict",
            "directed": True,
            "weight": 5,
            "label": "New York Times"
        },
        {
            "origin": "clinton/cp.s/en",
            "target": "trump/cp.s/en",
            "type": "conflict",
            "directed": True,
            "weight": 3,
            "label": "Washington Post"
        },
        {
            "origin": "democrats/cp.p/en",
            "target": "(+/b.am/. white/cp.s/en house/cp.s/en)",
            "type": "conflict",
            "directed": True,
            "weight": 1,
            "label": "Le Monde"
        },
        {
            "origin": "democrats/cp.p/en",
            "target": "rubio/cp.s/en",
            "type": "conflict",
            "directed": True,
            "weight": 1,
            "label": "Süddeutsche Zeitung"
        },
        {
            "origin": "democrats/cp.p/en",
            "target": "russia/cp.s/en",
            "type": "conflict",
            "directed": True,
            "weight": 1,
            "label": "Washington Post"
        },
        {
            "origin": "gop/cp.s/en",
            "target": "obama/cp.s/en",
            "type": "conflict",
            "directed": True,
            "weight": 3,
            "label": "The Guardian"
        },
        {
            "origin": "gop/cp.s/en",
            "target": "trump/cp.s/en",
            "type": "conflict",
            "directed": True,
            "weight": 1,
            "label": "New York Times"
        },
        {
            "origin": "mccain/cp.s/en",
            "target": "gop/cp.s/en",
            "type": "conflict",
            "directed": True,
            "weight": 1,
            "label": "New York Times"
        },
        {
            "origin": "mccain/cp.s/en",
            "target": "trump/cp.s/en",
            "type": "conflict",
            "directed": True,
            "weight": 8,
            "label": "Le Monde"
        },
        {
            "origin": "mccain/cp.s/en",
            "target": "trump/cp.s/en",
            "type": "conflict",
            "directed": True,
            "weight": 6,
            "label": "New York Times"
        },
        {
            "origin": "mcconnell/cp.s/en",
            "target": "obama/cp.s/en",
            "type": "conflict",
            "directed": True,
            "weight": 4,
            "label": "Le Monde"
        },
        {
            "origin": "mcconnell/cp.s/en",
            "target": "republicans/cp.p/en",
            "type": "conflict",
            "directed": True,
            "weight": 1,
            "label": "Le Monde"
        },
        {
            "origin": "mcconnell/cp.s/en",
            "target": "trump/cp.s/en",
            "type": "conflict",
            "directed": True,
            "weight": 1,
            "label": "The Guardian"
        },
        {
            "origin": "obama/cp.s/en",
            "target": "(+/b.am/. elizabeth/cp.s/en warren/cp.s/en)",
            "type": "conflict",
            "directed": True,
            "weight": 1,
            "label": "The Guardian"
        },
        {
            "origin": "obama/cp.s/en",
            "target": "(+/b.am/. scott/cp.s/en walker/cp.s/en)",
            "type": "conflict",
            "directed": True,
            "weight": 2,
            "label": "New York Times"
        },
        {
            "origin": "obama/cp.s/en",
            "target": "boehner/cp.s/en",
            "type": "conflict",
            "directed": True,
            "weight": 1,
            "label": "Washington Post"
        },
        {
            "origin": "obama/cp.s/en",
            "target": "democrats/cp.p/en",
            "type": "conflict",
            "directed": True,
            "weight": 3,
            "label": "New York Times"
        },
        {
            "origin": "obama/cp.s/en",
            "target": "gop/cp.s/en",
            "type": "conflict",
            "directed": True,
            "weight": 6,
            "label": "New York Times"
        },
        {
            "origin": "obama/cp.s/en",
            "target": "republicans/cp.p/en",
            "type": "conflict",
            "directed": True,
            "weight": 5,
            "label": "The Guardian"
        },
        {
            "origin": "obama/cp.s/en",
            "target": "russia/cp.s/en",
            "type": "conflict",
            "directed": True,
            "weight": 1,
            "label": "Le Monde"
        },
        {
            "origin": "obama/cp.s/en",
            "target": "trump/cp.s/en",
            "type": "conflict",
            "directed": True,
            "weight": 20,
            "label": "New York Times"
        },
        {
            "origin": "obama/cp.s/en",
            "target": "trump/cp.s/en",
            "type": "conflict",
            "directed": True,
            "weight": 12,
            "label": "Washington Post"
        },
        {
            "origin": "obama/cp.s/en",
            "target": "trump/cp.s/en",
            "type": "conflict",
            "directed": True,
            "weight": 8,
            "label": "The Guardian"
        },
        {
            "origin": "obama/cp.s/en",
            "target": "trump/cp.s/en",
            "type": "conflict",
            "directed": True,
            "weight": 3,
            "label": "üddeutsche Zeitung"
        },
        {
            "origin": "republicans/cp.p/en",
            "target": "obama/cp.s/en",
            "type": "conflict",
            "directed": True,
            "weight": 12,
            "label": "Süddeutsche Zeitung"
        },
        {
            "origin": "republicans/cp.p/en",
            "target": "trump/cp.s/en",
            "type": "conflict",
            "directed": True,
            "weight": 1,
            "label": "New York Times"
        },
        {
            "origin": "rubio/cp.s/en",
            "target": "obama/cp.s/en",
            "type": "conflict",
            "directed": True,
            "weight": 1,
            "label": "The Guardian"
        },
        {
            "origin": "rubio/cp.s/en",
            "target": "republicans/cp.p/en",
            "type": "conflict",
            "directed": True,
            "weight": 1,
            "label": "Süddeutsche Zeitung"
        },
        {
            "origin": "rubio/cp.s/en",
            "target": "trump/cp.s/en",
            "type": "conflict",
            "directed": True,
            "weight": 1,
            "label": "Le Monde"
        },
        {
            "origin": "russia/cp.s/en",
            "target": "obama/cp.s/en",
            "type": "conflict",
            "directed": True,
            "weight": 1,
            "label": "The Guardian"
        },
        {
            "origin": "russia/cp.s/en",
            "target": "trump/cp.s/en",
            "type": "conflict",
            "directed": True,
            "weight": 1,
            "label": "Le Monde"
        },
        {
            "origin": "russia/cp.s/en",
            "target": "trump/cp.s/en",
            "type": "conflict",
            "directed": True,
            "weight": 1,
            "label": "New York Times"
        },
        {
            "origin": "russia/cp.s/en",
            "target": "u_s_/cp.s/en",
            "type": "conflict",
            "directed": True,
            "weight": 3,
            "label": "Le Monde"
        },
        {
            "origin": "spicer/cp.s/en",
            "target": "obama/cp.s/en",
            "type": "conflict",
            "directed": True,
            "weight": 2,
            "label": "Süddeutsche Zeitung"
        },
        {
            "origin": "trump/cp.s/en",
            "target": "(+/b.am/. jeb/cp.s/en bush/cp.s/en)",
            "type": "conflict",
            "directed": True,
            "weight": 1,
            "label": "Le Monde"
        },
        {
            "origin": "trump/cp.s/en",
            "target": "clinton/cp.s/en",
            "type": "conflict",
            "directed": True,
            "weight": 15,
            "label": "Le Monde"
        },
        {
            "origin": "trump/cp.s/en",
            "target": "democrats/cp.p/en",
            "type": "conflict",
            "directed": True,
            "weight": 12,
            "label": "Süddeutsche Zeitung"
        },
        {
            "origin": "trump/cp.s/en",
            "target": "gop/cp.s/en",
            "type": "conflict",
            "directed": True,
            "weight": 6,
            "label": "Le Monde"
        },
        {
            "origin": "trump/cp.s/en",
            "target": "mccain/cp.s/en",
            "type": "conflict",
            "directed": True,
            "weight": 4,
            "label": "Süddeutsche Zeitung"
        },
        {
            "origin": "trump/cp.s/en",
            "target": "obama/cp.s/en",
            "type": "conflict",
            "directed": True,
            "weight": 38,
            "label": "Le Monde"
        },
        {
            "origin": "trump/cp.s/en",
            "target": "republicans/cp.p/en",
            "type": "conflict",
            "directed": True,
            "weight": 2,
            "label": "Le Monde"
        },
        {
            "origin": "trump/cp.s/en",
            "target": "russia/cp.s/en",
            "type": "conflict",
            "directed": True,
            "weight": 2,
            "label": "Washington Post"
        },
        {
            "origin": "u_s_/cp.s/en",
            "target": "russia/cp.s/en",
            "type": "conflict",
            "directed": True,
            "weight": 1,
            "label": "Washington Post"
        }
    ]
}


app = Flask(__name__)
CORS(app)


@app.route('/api/conflicts1')
def conflicts1():
    return jsonify(test_data)


@app.route('/api/conflicts2')
def conflicts2():
    data = copy.deepcopy(test_data)
    data['graph']['layout'] = 'predefined'
    for node in data['nodes']:
        node['x'] = random.random()
        node['y'] = random.random()
    return jsonify(data)
