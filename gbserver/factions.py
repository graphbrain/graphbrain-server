import operator


class Factions:
    def __init__(self, conflict_pairs):
        self.conflict_pairs = conflict_pairs
        self.edges = {}
        self.degrees = {}
        self.main_conflict = None
        self.factions = (set(), set())
        self._process()

    def _attacks_faction(self, actor, faction):
        for actor2 in self.factions[faction]:
            edge = tuple(sorted((actor, actor2)))
            if edge in self.edges:
                return True
        return False

    def _assign_faction(self, actor):
        if (self._attacks_faction(actor, 0) and
                not self._attacks_faction(actor, 1)):
            if actor in self.factions[1]:
                return False
            elif actor in self.factions[0]:
                return True
            else:
                self.factions[1].add(actor)
                return True
        elif (self._attacks_faction(actor, 1) and
                not self._attacks_faction(actor, 0)):
            if actor in self.factions[0]:
                return False
            elif actor in self.factions[1]:
                return True
            else:
                self.factions[0].add(actor)
                return True

        return False

    def _process(self):
        for pair in self.conflict_pairs:
            edge = tuple(sorted([x.label() for x in pair]))
            if edge not in self.edges:
                self.edges[edge] = 0
            actor1, actor2 = edge
            if actor1 not in self.degrees:
                self.degrees[actor1] = 0
            self.degrees[actor1] += 1
            if actor2 not in self.degrees:
                self.degrees[actor2] = 0
            self.degrees[actor2] += 1

        for edge in self.edges:
            self.edges[edge] = min([self.degrees[actor] for actor in edge])

        sorted_edges = sorted([(edge[0], edge[1], self.edges[edge])
                               for edge in self.edges],
                              key=operator.itemgetter(2), reverse=True)

        self.main_conflict = sorted_edges[0]
        self.factions[0].add(self.main_conflict[0])
        self.factions[1].add(self.main_conflict[1])

        changed = True
        while changed:
            changed = False
            for edge in sorted_edges[1:]:
                changed |= self._assign_faction(edge[0])
                changed |= self._assign_faction(edge[1])

    def faction(self, actor):
        if actor.label() in self.factions[0]:
            return 1
        elif actor.label() in self.factions[1]:
            return 2
        else:
            return 0
