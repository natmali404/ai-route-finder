import json

#Node: (name, outgoing_edges)
class Node:
    def __init__(self, name, lat, lon):
        self.name = name
        self.lat = lat
        self.lon = lon
        self.outgoing_edges = []
        
    def add_outgoing_edge(self, edge):
        self.outgoing_edges.append(edge)
        
    def get_outgoing_edges(self):
        return self.outgoing_edges
        
    def __eq__(self, other):
        if isinstance(other, Node):
            return self.name == other.name
        return False
    
    #arbitrary but necessary for heapq
    def __lt__(self, other):
        return self.name < other.name

    
    def __hash__(self):
        return hash(self.name)
        
    def __str__(self):
        return f"Node({self.name}, lat={self.lat}, lon={self.lon})"
    
    def __repr__(self):
        return f"Node(name='{self.name}', lat={self.lat}, lon={self.lon})"
    
     
       
        
#Edge: (start, end, line, dep_time, arr_time, travel_time)
class Edge:
    def __init__(self, start, end, line, dep_time, arr_time, travel_time):
        self.start = start
        self.end = end
        self.line = line
        self.dep_time = dep_time
        self.arr_time = arr_time
        self.travel_time = travel_time
        
    def __eq__(self, other):
        if isinstance(other, Edge):
            return self.start == other.start and self.end == other.end and self.line == other.line and self.dep_time == other.dep_time and self.arr_time == other.arr_time and self.travel_time == other.travel_time
        return False
    
    def __hash__(self):
        return hash((self.start, self.end, self.line, self.dep_time, self.arr_time, self.travel_time)) 
        
    def __str__(self):
        return f"Edge({self.start}, {self.end}, line={self.line}, dep_time={self.dep_time}, arr_time={self.arr_time}, travel_time={self.travel_time})"
    
    def __repr__(self):
        return (
            f"Edge(start={self.start.name}, end={self.end.name}, "
            f"line='{self.line}', dep_time={self.dep_time}, arr_time={self.arr_time}, travel_time={self.travel_time})"
        )



class Graph:
    def __init__(self, nodes, edges):
        self.nodes = nodes if nodes is not None else []
        self.edges = edges if edges is not None else []
        
    def add_node(self, node):
        self.nodes.append(node)
        
    def add_edge(self, edge):
        self.edges.append(edge)
        
    def get_node(self, name):
        for node in self.nodes:
            if node.name == name:
                return node
        return None
        
    def get_nodes(self):
        return self.nodes
    
    def get_edges(self):
        return self.edges
    
    def to_json(self, filename):
        """Serialize the graph to JSON file"""
        graph_data = {
            'nodes': [
                {
                    'name': node.name,
                    'lat': node.lat,
                    'lon': node.lon,
                    # Note: We don't serialize outgoing_edges to avoid circular references
                    # They will be reconstructed when loading
                } for node in self.nodes
            ],
            'edges': [
                {
                    'start': edge.start.name,
                    'end': edge.end.name,
                    'line': edge.line,
                    'dep_time': edge.dep_time,
                    'arr_time': edge.arr_time,
                    'travel_time': edge.travel_time
                } for edge in self.edges
            ]
        }
        with open(filename, 'w') as f:
            json.dump(graph_data, f, indent=2)
    
    @classmethod
    def from_json(cls, filename):
        """Deserialize the graph from JSON file"""
        with open(filename) as f:
            graph_data = json.load(f)
        
        # First create all nodes
        nodes = [
            Node(node['name'], node['lat'], node['lon'])
            for node in graph_data['nodes']
        ]
        
        # Create a mapping from node names to node objects
        node_dict = {node.name: node for node in nodes}
        
        # Then create all edges and reconstruct the graph structure
        edges = []
        for edge_data in graph_data['edges']:
            start_node = node_dict[edge_data['start']]
            end_node = node_dict[edge_data['end']]
            
            edge = Edge(
                start_node,
                end_node,
                edge_data['line'],
                edge_data['dep_time'],
                edge_data['arr_time'],
                edge_data['travel_time']
            )
            edges.append(edge)
            start_node.add_outgoing_edge(edge)
        
        return cls(nodes, edges)