from datetime import datetime
import csv
from graph import Graph, Node, Edge


def get_graph():
    unique_nodes = {}
    unique_edges = set()
    start_time = datetime.now()

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

    for edge in unique_edges:
        edge.start.add_outgoing_edge(edge)
        
    end_time = datetime.now()
    log(f"Graph initialization execution time: {end_time - start_time} seconds")
        
    return Graph(list(unique_nodes.values()), list(unique_edges))

#time helpers
def time_to_minutes(time_str):
    parts = list(map(int, time_str.split(':')))
    h = parts[0]
    m = parts[1]
    
    return (h % 24) * 60 + m


def minutes_to_time(minutes):
    h = minutes // 60 % 24
    m = minutes % 60
    return f"{h:02d}:{m:02d}:00"

def format_time(timestamp):
    return timestamp.strftime("%Y-%m-%d %H:%M:%S.%f")[:-4]

def log(message):
    print(f"[{format_time(datetime.now())}] {message}")
    
    
def reconstruct_path(previous, starting_stop, destination_stop):
    """ Traces the path back from the destination to the start and returns a list of steps. """
    start_time = datetime.now()
    path = []
    current = destination_stop
    final_arrival_time = None
    while current != starting_stop:
        prev_node, edge_used, line_used = previous.get(current, (None, None, None))
        if prev_node is None:
            return None  # No valid path found
        path.append((prev_node, edge_used, current, line_used))
        current = prev_node
        
        # Save the first (last in reversed order) arrival time
        if final_arrival_time is None:
            final_arrival_time = time_to_minutes(edge_used.arr_time)
    path.reverse()  # Reverse to get start-to-end order
    
    stop_algorithm_time = datetime.now()
    log(f"Path reconstruction execution time: {stop_algorithm_time - start_time} seconds")
    return path, final_arrival_time

#chatgpt formatting
def print_path(path, starting_stop_name, start_time, total_travel_time):
    """ Prints the formatted shortest path based on the reconstructed path list. """
    if path is None:
        print("No complete path found!")
        return
    
    print(f"\nShortest path from {starting_stop_name} at {start_time}:")
    print(f"Start at {path[0][0].name} (Time: {start_time})")
    
    current_line = None
    for prev_node, edge, current_node, line in path:
        if line != current_line:
            print(f"  → Change to line {line} at {prev_node.name}")
            current_line = line
        print(f"    → Depart at {edge.dep_time} from {prev_node.name}")
        print(f"    → Arrive at {current_node.name} at {edge.arr_time} ({edge.travel_time} mins)")
    
    print(f"\nTotal travel time: {total_travel_time} minutes")
    
    
def calculate_total_travel_time(start_time, final_arrival_time):
    """ Calculates the total travel time in minutes. """
    if final_arrival_time < start_time:
        final_arrival_time += 24 * 60  # Adjust for next day
    
    return final_arrival_time - start_time