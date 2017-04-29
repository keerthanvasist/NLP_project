
# from abc import ABCMeta, abstractmethod




class Graph():
    """
    Implementation of an undirected graph, based on Pygraph
    """

    WEIGHT_ATTRIBUTE_NAME = "weight"
    DEFAULT_WEIGHT = 0

    LABEL_ATTRIBUTE_NAME = "label"
    DEFAULT_LABEL = ""

    def __init__(self):
        # Metadata about edges
        self.edge_properties = {}    # Mapping: Edge -> Dict mapping, lablel-> str, wt->num
        self.edge_attr = {}          # Key value pairs: (Edge -> Attributes)
        # Metadata about nodes
        self.node_attr = {}          # Pairing: Node -> Attributes
        self.node_neighbors = {}     # Pairing: Node -> Neighbors

    def has_edge(self, edge):
        # print "has edge"
        u,v = edge
        return (u,v) in self.edge_properties and (v,u) in self.edge_properties

    def edge_weight(self, edge):
        # print "edge weight"
        return self.get_edge_properties( edge ).setdefault( self.WEIGHT_ATTRIBUTE_NAME, self.DEFAULT_WEIGHT )

    def neighbors(self, node):
        # print "neighbors"
        return self.node_neighbors[node]

    def has_node(self, node):
        # print "has node"
        return node in self.node_neighbors

    def add_edge(self, edge, wt=1, label='', attrs=[]):
        # print "add edge"
        u, v = edge
        if (v not in self.node_neighbors[u] and u not in self.node_neighbors[v]):
            self.node_neighbors[u].append(v)
            if (u != v):
                self.node_neighbors[v].append(u)

            self.add_edge_attributes((u,v), attrs)
            self.set_edge_properties((u, v), label=label, weight=wt)
        else:
            raise ValueError("Edge (%s, %s) already in graph" % (u, v))

    def add_node(self, node, attrs=None):
        # print "add node"
        if attrs is None:
            attrs = []
        if (not node in self.node_neighbors):
            self.node_neighbors[node] = []
            self.node_attr[node] = attrs
        else:
            raise ValueError("Node %s already in graph" % node)

    def nodes(self):
        # print "nodes"
        return list(self.node_neighbors.keys())

    

    def del_node(self, node):
        # print "del node"
        for each in list(self.neighbors(node)):
            if (each != node):
                self.del_edge((each, node))
        del(self.node_neighbors[node])
        del(self.node_attr[node])

    # Helper methods
    def get_edge_properties(self, edge):
        # print "get edge prop"
        return self.edge_properties.setdefault( edge, {} )

    def add_edge_attributes(self, edge, attrs):
        # print "add egde attrs"
        for attr in attrs:
            self.add_edge_attribute(edge, attr)

   

 

    def set_edge_properties(self, edge, **properties ):
        # print "set edge props"
        self.edge_properties.setdefault( edge, {} ).update( properties )
        if (edge[0] != edge[1]):
            self.edge_properties.setdefault((edge[1], edge[0]), {}).update( properties )




def build_graph(sequence):
    # print "Called build graph!!!"
    graph = Graph()
    for item in sequence:
        if not graph.has_node(item):
            graph.add_node(item)
    return graph


def remove_unreachable_nodes(graph):
    # print "Called remove unreachable nodes!!"

    for node in graph.nodes():
        if sum(graph.edge_weight((node, other)) for other in graph.neighbors(node)) == 0:
            graph.del_node(node)
