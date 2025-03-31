from datetime import datetime
import heapq
from utils import time_to_minutes, print_path, log, reconstruct_path, print_path, calculate_total_travel_time
from graph import Graph, Node, Edge


#CURRENT BEST VERSION but trying to modify
def find_dijkstra_path(graph, starting_stop_name, destination_stop_name, start_time):
    start_algorithm_time = datetime.now()
    starting_stop = graph.get_node(starting_stop_name)
    destination_stop = graph.get_node(destination_stop_name)
    
    if starting_stop is None or destination_stop is None:
        print("Starting stop not found")
        return
    
    start_total = time_to_minutes(start_time)
    
    distance = {}
    previous = {}
    transfers = {}
    for node in graph.get_nodes():
        distance[node] = float('inf')
        previous[node] = (None, None, None)
        transfers[node] = float('inf')
    distance[starting_stop] = 0
    transfers[starting_stop] = 0
    
    #priority queue: (transfer_count, total_cost, stop, current_line, current_time)
    priority_queue = [(0, 0, starting_stop, None, start_total)]  
    
    while priority_queue:
        current_transfers, current_cost, current_stop, current_line, current_time = heapq.heappop(priority_queue)
        
        # ?
        if current_stop == destination_stop:
            break

        for neighbor_edge in current_stop.get_outgoing_edges():
            
            dep_total = time_to_minutes(neighbor_edge.dep_time)
            
            if dep_total < current_time: #consider only edges that depart after current time?
                continue
            
            #something could be wrong here - maybe?
            wait_time = dep_total - current_time # if current_stop != starting_stop else 0 #<- better results but RANDOM
            
            #penalties
            new_transfer_count = current_transfers + (1 if (current_line is not None and neighbor_edge.line != current_line) else 0)
            transfer_penalty = 20 if (current_line is not None and neighbor_edge.line != current_line) else 0
            
            total_edge_cost = neighbor_edge.travel_time + wait_time + transfer_penalty
            new_cost = current_cost + total_edge_cost
            
            arr_total = time_to_minutes(neighbor_edge.arr_time)
            
            if new_cost < distance[neighbor_edge.end]:
                distance[neighbor_edge.end] = new_cost
                transfers[neighbor_edge.end] = new_transfer_count
                previous[neighbor_edge.end] = (current_stop, neighbor_edge, neighbor_edge.line)
                heapq.heappush(priority_queue, (new_transfer_count, new_cost, neighbor_edge.end, neighbor_edge.line, arr_total)) #(total_cost, current_stop, current_line, current_time)
                
    stop_algorithm_time = datetime.now()
    log(f"Dijkstra execution time: {stop_algorithm_time - start_algorithm_time} seconds")
    #print(path)
    path, final_arrival_time = reconstruct_path(previous, starting_stop, destination_stop)
    total_travel_time = calculate_total_travel_time(start_total, final_arrival_time)
    print_path(path, starting_stop_name, start_time, total_travel_time, distance[destination_stop])