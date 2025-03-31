import heapq
from datetime import datetime
from utils import time_to_minutes, print_path, log, reconstruct_path, calculate_total_travel_time
from math import radians, sin, cos, sqrt, atan2

#to do: avg speeds and deg to m numbers go to consts.

def euclidean_distance(node1, node2):
    return sqrt((node1.lat - node2.lat) ** 2 + (node1.lon - node2.lon) ** 2) * 111000 #deg to m

def haversine_distance(node1, node2):
    R = 6371  #earth radius (km)
    lat1, lon1 = radians(node1.lat), radians(node1.lon)
    lat2, lon2 = radians(node2.lat), radians(node2.lon)
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c * 1000  #meters


def manhattan_distance(node1, node2):
    return (abs(node1.lat - node2.lat) + abs(node1.lon - node2.lon)) * 111000 #deg to m


def find_a_star_path(graph, start_name, dest_name, start_time, heuristic='euclidean'):
    start_algorithm_time = datetime.now()
    start_node = graph.get_node(start_name)
    dest_node = graph.get_node(dest_name)
    
    if start_node is None or dest_node is None:
        print("Starting or destination stop not found")
        return
    
    start_total = time_to_minutes(start_time)
    distance = {node: float('inf') for node in graph.get_nodes()}
    previous = {node: (None, None, None) for node in graph.get_nodes()}
    transfers = {node: float('inf') for node in graph.get_nodes()}
    distance[start_node] = 0
    transfers[start_node] = 0
    
    if heuristic == 'euclidean': #read more about this to know what it does
        heuristic_function = lambda node: euclidean_distance(node, dest_node) / 50  # avg speed 50 km/h
    elif heuristic == 'manhattan':
        heuristic_function = lambda node: manhattan_distance(node, dest_node) / 50
    else:
        heuristic_function = lambda node: haversine_distance(node, dest_node) / 50
        
    
    priority_queue = [(0 + heuristic_function(start_node), 0, start_node, None, start_total)]
    
    while priority_queue:
        _, current_cost, current_stop, current_line, current_time = heapq.heappop(priority_queue)
        
        if current_stop == dest_node:
            break
        
        for edge in current_stop.get_outgoing_edges():
            dep_total = time_to_minutes(edge.dep_time)
            if dep_total < current_time:
                continue
            
            wait_time = dep_total - current_time
            new_transfer_count = transfers[current_stop] + (1 if current_line and edge.line != current_line else 0)
            transfer_penalty = 20 if current_line and edge.line != current_line else 0
            
            total_edge_cost = edge.travel_time + wait_time + transfer_penalty
            new_cost = current_cost + total_edge_cost
            arr_total = time_to_minutes(edge.arr_time)
            
            #closedList
            if new_cost < distance[edge.end]:
                distance[edge.end] = new_cost
                transfers[edge.end] = new_transfer_count
                previous[edge.end] = (current_stop, edge, edge.line)
                estimated_total_cost = new_cost + heuristic_function(edge.end) #f = g + h
                heapq.heappush(priority_queue, (estimated_total_cost, new_cost, edge.end, edge.line, arr_total))
    
    stop_algorithm_time = datetime.now()
    log(f"A* execution time: {stop_algorithm_time - start_algorithm_time} seconds")
    
    path, final_arrival_time = reconstruct_path(previous, start_node, dest_node)
    total_travel_time = calculate_total_travel_time(start_total, final_arrival_time)
    print(f'PATH: {path}')
    return path, total_travel_time
    # 
    # 
