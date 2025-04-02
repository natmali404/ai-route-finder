from datetime import datetime
import heapq
from utils import time_to_minutes, print_path, log, reconstruct_path, print_path, calculate_total_travel_time
from graph import Graph, Node, Edge


def find_dijkstra_path(graph, starting_stop_name, destination_stop_name, start_time, criteria):
    start_algorithm_time = datetime.now()
    starting_stop = graph.get_node(starting_stop_name)
    destination_stop = graph.get_node(destination_stop_name)
    
    if not starting_stop or not destination_stop:
        print("Error: Invalid start or destination stop")
        return None, None
    
    start_total = time_to_minutes(start_time)

    distance = {node: float('inf') for node in graph.get_nodes()}
    previous = {node: (None, None, None) for node in graph.get_nodes()}
    earliest_arrival = {node: float('inf') for node in graph.get_nodes()}
    
    distance[starting_stop] = 0
    earliest_arrival[starting_stop] = start_total
    
    visited = set()
    
    #priority queue: (transfer_count, earliest_arrival, total_cost, current_stop, current_line)
    priority_queue = [(0, 0, start_total, starting_stop, None)]
    heapq.heapify(priority_queue)
    
    while priority_queue:
        # current_transfers, current_cost, current_stop, current_line, current_time = heapq.heappop(priority_queue)
        current_transfers, current_cost, current_time, current_stop, current_line = heapq.heappop(priority_queue)
        
        if current_stop in visited and distance[current_stop] < current_cost:
            continue
        
        visited.add(current_stop)
        
        #skip if we've already found a better path to this node
        if current_time > earliest_arrival[current_stop]:
            continue
        
        # ?destination found
        if current_stop == destination_stop:
            break

        for neighbor_edge in current_stop.get_outgoing_edges():
            
            dep_total = time_to_minutes(neighbor_edge.dep_time)
            arr_total = time_to_minutes(neighbor_edge.arr_time)
            
            if dep_total < current_time: #consider only edges that depart after current time?
                continue
            
            #something could be wrong here - maybe?
            wait_time = dep_total - current_time # if current_stop != starting_stop else 0 #<- better results but RANDOM
            
            #penalties
            new_transfer_count = current_transfers + (1 if (current_line is not None and neighbor_edge.line != current_line) else 0)
    
            # transfer_penalty = 20 if (current_line is not None and neighbor_edge.line != current_line) else 0
            
            if criteria == 't':  #time-optimized
                total_edge_cost = (10 if (current_line and neighbor_edge.line != current_line) else 0) + neighbor_edge.travel_time + wait_time
            elif criteria == 'p':  #transfer-optimized
                total_edge_cost = (100*new_transfer_count if (current_line and neighbor_edge.line != current_line) else 0) + wait_time + neighbor_edge.travel_time
            
            new_cost = current_cost + total_edge_cost
            
            # if neighbor_edge.line == current_line and time_to_minutes(neighbor_edge.dep_time) == current_time:
            #     new_cost -= 2
            
            if new_cost < distance[neighbor_edge.end]:
                distance[neighbor_edge.end] = new_cost
                earliest_arrival[neighbor_edge.end] = arr_total
                # transfers[neighbor_edge.end] = new_transfer_count
                previous[neighbor_edge.end] = (current_stop, neighbor_edge, neighbor_edge.line)
                heapq.heappush(priority_queue, (new_transfer_count, new_cost, arr_total, neighbor_edge.end, neighbor_edge.line))
                
    stop_algorithm_time = datetime.now()
    log(f"Dijkstra execution time: {stop_algorithm_time - start_algorithm_time} seconds")
    
    
    path, final_arrival_time = reconstruct_path(previous, starting_stop, destination_stop)
    if path is None:
        print("Error reconstructing path")
        return None, None
    
    total_travel_time = calculate_total_travel_time(start_total, final_arrival_time)
    #print_path(path, starting_stop_name, start_time, total_travel_time)
    
    return path, total_travel_time

