class ChordGraph:

    def __init__(self):
        self.G = dict()
        self.occs = dict()
    
    def add_edge(self, nodeFrom, nodeTo):
        if nodeFrom not in self.G.keys():
            self.G[nodeFrom] = dict()
        
        if nodeTo not in self.G[nodeFrom].keys():
            self.G[nodeFrom][nodeTo] = 0

        self.G[nodeFrom][nodeTo] += 1

    def add_occurrence(self, node):
        if node not in self.occs.keys():
            self.occs[node] = 1
        else: self.occs[node] += 1
            

    def finish(self):
        for parent in self.G.keys():
            total = 0
            for child in self.G[parent].keys():
                total += self.G[parent][child]
            for child in self.G[parent].keys():
                self.G[parent][child] /= total

    def debug(self):
        l = []
        for parent in self.G.keys():
            l.append(parent)

        l = sorted(l, key = lambda x: -self.occs[x])

        out = ""
        for parent in l:
            out += parent + "\n"
            for child in self.__get_children_sorted(parent):
                out += "\t{0}: {1:0.2f}%\n".format(child[0], child[1] * 100)

        return out
            
    
    def __get_children_sorted(self, node):
        l = []
        for child in self.G[node].keys():
                l.append((child, self.G[node][child]))
        l.sort(key=lambda x: -x[1])
        return sorted(l, key = lambda x: -x[1])