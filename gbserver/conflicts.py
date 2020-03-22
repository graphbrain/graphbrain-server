from collections import Counter, defaultdict
from graphbrain.meaning.corefs import main_coref
from graphbrain.meaning.concepts import all_concepts, has_proper_concept


conflict_topic_triggers = {'of/t/en', 'over/t/en', 'against/t/en', 'for/t/en'}


actor_degrees = None
all_topics = None


def actors(hg):
    global actor_degrees
    if actor_degrees is None:
        actor_degrees = Counter()
        for conflict_edge in hg.search('(conflict/p/. * * *)'):
            actor1 = main_coref(hg, conflict_edge[1])
            actor2 = main_coref(hg, conflict_edge[2])
            actor_degrees[actor1] += 1
            actor_degrees[actor2] += 1
    return actor_degrees


def is_valid(hg, actor):
    acts = actors(hg)
    return actor.connector_type() != 'b+' and acts[actor] > 1


def conflict_topics(hg):
    global all_topics
    if all_topics is None:
        all_topics = Counter()
        topics = Counter()

        for conflict_edge in hg.search('(conflict/p/. * * *)'):
            actor1 = main_coref(hg, conflict_edge[1])
            actor2 = main_coref(hg, conflict_edge[2])
            if is_valid(hg, actor1) and is_valid(hg, actor2):
                edge = conflict_edge[3]
                for item in edge[1:]:
                    if item.type()[0] == 's':
                        if item[0].to_str() in conflict_topic_triggers:
                            for concept in all_concepts(item[1]):
                                topic = main_coref(hg, concept)
                                topics[topic] += 1
        for topic, weight in topics.most_common():
            if weight > 1 and has_proper_concept(topic):
                all_topics[topic] = weight
    return all_topics


def conflicts_by_topic(hg, topic):
    conflicts = defaultdict(list)

    for conflict_edge in hg.search('(conflict/p/. * * *)'):
        actor1 = main_coref(hg, conflict_edge[1])
        actor2 = main_coref(hg, conflict_edge[2])
        if is_valid(hg, actor1) and is_valid(hg, actor2):
            edge = conflict_edge[3]
            for item in edge[1:]:
                if item.type()[0] == 's':
                    if item[0].to_str() in conflict_topic_triggers:
                        topics = list(main_coref(hg, concept)
                                      for concept in all_concepts(item[1]))
                        if topic in topics:
                            all_topics = conflict_topics(hg)
                            other_topics = set()
                            for t in topics:
                                if t in all_topics and t != topic:
                                    other_topics.add(t)
                            text = hg.get_str_attribute(edge, 'text')
                            conflict_data = {'text': text,
                                             'other_topics': other_topics}
                            conflicts[(actor1, actor2)].append(conflict_data)
    return conflicts
