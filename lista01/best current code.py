import csv
import heapq
import random

#time helpers
def time_to_minutes(time_str):
    """Convert time string (HH:MM or HH:MM:SS) to minutes since midnight, handling times > 23:59"""
    parts = list(map(int, time_str.split(':')))
    h = parts[0]
    m = parts[1]
    
    # Handle times that wrap around midnight (e.g., 24:05 becomes 00:05)
    return (h % 24) * 60 + m


def minutes_to_time(minutes):
    h = minutes // 60 % 24
    m = minutes % 60
    return f"{h:02d}:{m:02d}:00"


#path, cost = simplified_dijkstra(G, "PL. GRUNWALDZKI", "Wrocławski Park Przemysłowy", "23:49")
#CURRENT BEST VERSION!! 23:06 
def find_dijkstra_path(graph, starting_stop_name, destination_stop_name, start_time):
    #if gdy cos jest koncowym przystankiem to spradzamy czy wsyzstkie krawedzie byly sprawdzone
    
    #firstly, check if the stop even exists
    starting_stop = graph.get_node(starting_stop_name)
    destination_stop = graph.get_node(destination_stop_name)
    if starting_stop is None:
        print("Starting stop not found")
        return
    
    start_total = time_to_minutes(start_time)
    
    distance = {}
    previous = {}
    for node in graph.get_nodes():
        distance[node] = float('inf')
        previous[node] = (None, None, None)  # (prev_node, edge_used, current_line)
    distance[starting_stop] = 0
    
    #priority queue
    visited = set()
    priority_queue = [(0, start_total, starting_stop, None)] #(total_cost, current_time, current_stop, current_line)
    
    while priority_queue:
        current_cost, current_time, current_stop, current_line = heapq.heappop(priority_queue)
        if current_stop in visited:
            continue

        visited.add(current_stop)
        
        if current_stop == destination_stop:
            break

        
        
        for neighbor_edge in current_stop.get_outgoing_edges():
            
            dep_total = time_to_minutes(neighbor_edge.dep_time)
            
            if dep_total < current_time: #consider only edges that depart after current time
                continue
            
            wait_time = dep_total - current_time #do current cost nalezy dodac czas oczekiwania na przystanku ale moze nie
            
            transfer_penalty = 20 if (current_line is not None and neighbor_edge.line != current_line) else 0
            
            total_edge_cost = wait_time + neighbor_edge.travel_time + transfer_penalty
            new_cost = current_cost + total_edge_cost
            
            next_stop = neighbor_edge.end
            next_stop_cost = distance[next_stop]
            #additional_cost
            
            arr_total = time_to_minutes(neighbor_edge.arr_time)
            
            if new_cost < distance[neighbor_edge.end]:
                distance[neighbor_edge.end] = new_cost
                previous[neighbor_edge.end] = (current_stop, neighbor_edge, neighbor_edge.line)
                heapq.heappush(priority_queue, (new_cost, arr_total, neighbor_edge.end, neighbor_edge.line))

        # Path reconstruction with line and time info
    print(f"\nShortest path from {starting_stop_name} to {destination_stop_name} at {start_time}:")
    
    path = []
    current = destination_stop
    while current != starting_stop:
        prev_node, edge_used, line_used = previous[current]  # Now unpacking 3 values
        if prev_node is None:  # No path exists
            print("No complete path found!")
            return
        path.append((prev_node, edge_used, current, line_used))
        current = prev_node
    
    # Print in chronological order
    path.reverse()
    print(f"Start at {starting_stop.name} (Time: {start_time})")
    current_line = None
    for prev_node, edge, current_node, line in path:
        if line != current_line:
            print(f"  → Change to line {line} at {prev_node.name}")
            current_line = line
        print(f"    → Depart at {edge.dep_time} from {prev_node.name}")
        print(f"    → Arrive at {current_node.name} at {edge.arr_time} ({edge.travel_time} mins)")
    
    print(f"\nTotal travel time: {distance[destination_stop]} minutes")
    
    
#old/experimental
def old_find_dijkstra_path(graph, starting_stop_name, destination_stop_name, start_time):
    #if gdy cos jest koncowym przystankiem to spradzamy czy wsyzstkie krawedzie byly sprawdzone
    
    #firstly, check if the stop even exists
    starting_stop = graph.get_node(starting_stop_name)
    destination_stop = graph.get_node(destination_stop_name)
    if starting_stop is None:
        print("Starting stop not found")
        return
    
    #distance table
    distance = {}
    for node in graph.get_nodes():
        distance[node] = float('inf') if node != starting_stop else 0
        
    #previous node - now stores (node, edge) pairs
    previous = {}
    for node in graph.get_nodes():
        previous[node] = (None, None)  # (previous_node, edge_used)
    
    #priority queue
    visited = set()
    priority_queue = [(0, start_time, starting_stop)]
    
    while priority_queue:
        current_cost, current_time, current_stop  = heapq.heappop(priority_queue)
        if current_stop in visited:
            continue

        visited.add(current_stop)
        
        if current_stop == destination_stop:
            break

        #do current cost nalezy dodac czas oczekiwania na przystanku
        
        for neighbor_edge in current_stop.get_outgoing_edges():
            next_stop = neighbor_edge.end
            next_stop_cost = distance[next_stop]
            # print(pd.to_datetime(neighbor_edge.dep_time)) #2025-03-24 07:14:00
            # print(pd.to_datetime(current_time)) #2025-03-24 15:49:00
            #get time difference in int (minutes) from the two timestamps above, while handling the case when the time difference is negative
            #jak sie zegar obraca wokol doby to dupa
            additional_wait_cost = (pd.to_datetime(neighbor_edge.dep_time) - pd.to_datetime(current_time)).seconds // 60
            if additional_wait_cost < 0:
                print(additional_wait_cost)
                # additional_wait_cost = 1440 + additional_wait_cost
            
            if current_cost + neighbor_edge.travel_time + additional_wait_cost < next_stop_cost:
                distance[next_stop] = current_cost + neighbor_edge.travel_time + additional_wait_cost
                previous[next_stop] = (current_stop, neighbor_edge)  # Store edge info
                heapq.heappush(priority_queue, (distance[next_stop], neighbor_edge.arr_time, next_stop))

    # Path reconstruction with line and time info
    print(f"\nShortest path from {starting_stop_name} to {destination_stop_name} at {start_time}:")
    
    path = []
    current = destination_stop
    while current != starting_stop:
        prev_node, edge_used = previous[current]
        if prev_node is None:  # No path exists
            print("No complete path found!")
            return
        path.append((prev_node, edge_used, current))
        current = prev_node
    
    # Print in chronological order
    path.reverse()
    print(f"Start at {starting_stop.name} (Time: {start_time})")
    for prev_node, edge, current_node in path:
        print(f"  → Take line {edge.line} at {edge.dep_time} from {prev_node.name}")
        print(f"    → Arrive at {current_node.name} at {edge.arr_time} ({edge.travel_time} mins)")
    
    print(f"\nTotal travel time: {distance[destination_stop]} minutes")

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
    
    def __lt__(self, other):
        #arbitrary but necessary for heapq
        return self.name < other.name

    
    def __hash__(self):
        return hash(self.name)
        
    def __str__(self):
        return f"Node({self.name}, lat={self.lat}, lon={self.lon})"
        
        

#MOD: KRAWEDZ MA LISTE CZASOW?

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



def get_graph():
    unique_nodes = {}
    unique_edges = set()

    with open('connection_graph.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for data_row in reader:
            try:
                start = data_row["start_stop"]
                end = data_row["end_stop"]
                line = data_row["line"]
                dep_time = data_row["departure_time"]
                arr_time = data_row["arrival_time"]
                start_stop_lat = float(data_row["start_stop_lat"])
                start_stop_lon = float(data_row["start_stop_lon"])
                end_stop_lat = float(data_row["end_stop_lat"])
                end_stop_lon = float(data_row["end_stop_lon"])

                dep_h, dep_m, dep_s = map(int, dep_time.split(":"))
                arr_h, arr_m, arr_s = map(int, arr_time.split(":"))
                dep_mins = dep_h * 60 + dep_m
                arr_mins = arr_h * 60 + arr_m
                travel_time = abs(arr_mins - dep_mins)
                
                if dep_h >= 24:
                    dep_time = f"{(dep_h-24):02d}:{(dep_m):02d}:00"
                
                if arr_h >= 24:
                    arr_time = f"{(arr_h-24):02d}:{(arr_m):02d}:00"

                # Get or create nodes
                if start not in unique_nodes:
                    unique_nodes[start] = Node(start, start_stop_lat, start_stop_lon)
                if end not in unique_nodes:
                    unique_nodes[end] = Node(end, end_stop_lat, end_stop_lon)
                
                nodeA = unique_nodes[start]
                nodeB = unique_nodes[end]
                
                edge = Edge(nodeA, nodeB, line, dep_time, arr_time, travel_time)
                unique_edges.add(edge)
                
            except Exception as e:
                print(f"Error in line {data_row}: {e}")

    # Now add the outgoing edges
    for edge in unique_edges:
        edge.start.add_outgoing_edge(edge)
        
    return Graph(list(unique_nodes.values()), list(unique_edges))
    
    
    

#debug
def print_random_nodes_with_edges(graph, num_nodes=10):
    # Make sure there are at least 'num_nodes' nodes in the graph
    if len(graph.nodes) < num_nodes:
        print(f"Graph has fewer than {num_nodes} nodes. Printing all nodes instead.")
        num_nodes = len(graph.nodes)
    
    # Randomly select 'num_nodes' nodes from the graph
    random_nodes = random.sample(graph.nodes, num_nodes)
    
    for node in random_nodes:
        print(f"\nNode: {node}")
        print(f"Outgoing edges from {node.name}:")
        for edge in node.get_outgoing_edges():
            print(f"  - {edge}")
            

def print_edges_of_node(graph, nodename):
    node = graph.get_node(nodename)
    print(f"\nNode: {node}")
    print(f"Outgoing edges from {node.name}:")
    for edge in node.get_outgoing_edges():
        print(f"  - {edge}")
   


if __name__ == "__main__":
    print("Begin graph initialization...")
    graph = get_graph()
    # print("\nEdges:")
    # for edge in graph.edges:
    #     print(edge)
    # print("\nNodes:")
    # for node in graph.nodes:
    #     print(node)
    print(f"Graph has {len(graph.nodes)} nodes and {len(graph.edges)} edges.")
    for edge in graph.edges:
        if edge.start == "most Grunwaldzki" and edge.end == "PL. GRUNWALDZKI":
            print(edge)
    #print_random_nodes_with_edges(graph)
    #print_edges_of_node(graph, "PL. GRUNWALDZKI")
    find_dijkstra_path(graph, "PL. GRUNWALDZKI", "Wrocławski Park Przemysłowy", "15:49")
    find_dijkstra_path(graph, "Stalowa", "PL. GRUNWALDZKI", "15:49")
    