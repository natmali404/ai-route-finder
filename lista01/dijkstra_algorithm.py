from datetime import datetime
import heapq
from utils import time_to_minutes, print_path, log, reconstruct_path, print_path, calculate_total_travel_time
from graph import Graph, Node, Edge
import math


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
        
        # ?
        if current_stop == destination_stop:
            break

        for neighbor_edge in current_stop.get_outgoing_edges():
            
            dep_total = time_to_minutes(neighbor_edge.dep_time)
            arr_total = time_to_minutes(neighbor_edge.arr_time)
            
            if dep_total < current_time: #consider only edges that depart after current time?
                continue
            
            # if current_stop.name == "PL. GRUNWALDZKI":
            #     print(neighbor_edge.dep_time)
                
                
            #something could be wrong here - maybe?
            wait_time = dep_total - current_time # if current_stop != starting_stop else 0 #<- better results but RANDOM
            
            #penalties
            new_transfer_count = current_transfers + (1 if (current_line is not None and neighbor_edge.line != current_line) else 0)
    
            # transfer_penalty = 20 if (current_line is not None and neighbor_edge.line != current_line) else 0
            
            if criteria == 't':  # Time-optimized
                total_edge_cost = (10 if (current_line and neighbor_edge.line != current_line) else 0) + neighbor_edge.travel_time + wait_time
            elif criteria == 'p':  # Transfer-optimized
                total_edge_cost = (100*new_transfer_count if (current_line and neighbor_edge.line != current_line) else 0) + wait_time + neighbor_edge.travel_time
            
            #total_edge_cost = neighbor_edge.travel_time + wait_time + transfer_penalty
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
















def broken_find_dijkstra_path(graph, starting_stop_name, destination_stop_name, start_time, criteria):
    start_algorithm_time = datetime.now()
    starting_stop = graph.get_node(starting_stop_name)
    destination_stop = graph.get_node(destination_stop_name)
    
    if starting_stop is None or destination_stop is None:
        print("Starting stop not found")
        return
    
    start_total = time_to_minutes(start_time)
    
    distance = {}
    previous = {}
    transfers = {} #change this and the queue to sart with current time
    arrival_time = {} #prevent an earlier departure appearing later in the path
    for node in graph.get_nodes():
        distance[node] = float('inf')
        previous[node] = (None, None, None)
        transfers[node] = float('inf')
        arrival_time[node] = float('inf')
    distance[starting_stop] = 0
    transfers[starting_stop] = 0
    arrival_time[starting_stop] = start_total
    
    #priority queue: (transfer_count, total_cost, dep_total, stop, current_line, current_time)
    priority_queue = [(0, 0, start_total, starting_stop, None, start_total)]

    
    while priority_queue:
        current_transfers, current_cost, dep_time, current_stop, current_line, current_time = heapq.heappop(priority_queue)
        
        # ?
        if current_stop == destination_stop:
            break

        for neighbor_edge in current_stop.get_outgoing_edges():
            
            dep_total = time_to_minutes(neighbor_edge.dep_time)
            
            if dep_total < current_time:
                continue
            if dep_total > current_time + 60:  # Don't skip too far ahead
                continue

            
            #something could be wrong here - maybe?
            # wait_time = dep_total - current_time # if current_stop != starting_stop else 0 #<- better results but RANDOM
            
            #penalties
            new_transfer_count = current_transfers + (1 if (current_line is not None and neighbor_edge.line != current_line) else 0)
            
            if criteria == 't':  # Time-optimized
                wait_time = dep_total - current_time
                total_edge_cost = neighbor_edge.travel_time + wait_time
            elif criteria == 'p':  # Transfer-optimized
                wait_time = dep_total - current_time if current_stop != starting_stop else 0
                total_edge_cost = (100 if (current_line and neighbor_edge.line != current_line) else 0) + wait_time + neighbor_edge.travel_time
            
            #total_edge_cost = neighbor_edge.travel_time + wait_time + transfer_penalty
            new_cost = current_cost + total_edge_cost
            
            arr_total = time_to_minutes(neighbor_edge.arr_time)
            
            if new_cost < distance[neighbor_edge.end]: # and arr_total >= arrival_time[current_stop]
                distance[neighbor_edge.end] = new_cost
                transfers[neighbor_edge.end] = new_transfer_count
                previous[neighbor_edge.end] = (current_stop, neighbor_edge, neighbor_edge.line)
                arrival_time[neighbor_edge.end] = arr_total  # <-- Ensure we only push forward in time
                if current_stop == starting_stop:
                    print(neighbor_edge.end.name, neighbor_edge.dep_time, neighbor_edge.arr_time, neighbor_edge.travel_time, new_cost)
                heapq.heappush(priority_queue, (new_transfer_count, new_cost, dep_total, neighbor_edge.end, neighbor_edge.line, arr_total))


                
    stop_algorithm_time = datetime.now()
    log(f"Dijkstra execution time: {stop_algorithm_time - start_algorithm_time} seconds")
    
    
    path, final_arrival_time = reconstruct_path(previous, starting_stop, destination_stop)
    if path is None:
        print("Error reconstructing path")
        return None, None
    
    total_travel_time = calculate_total_travel_time(start_total, final_arrival_time)
    print_path(path, starting_stop_name, start_time, total_travel_time)
    
    return path, total_travel_time


#experimental
def xd_find_dijkstra_path(graph, starting_stop_name, destination_stop_name, start_time, criteria):
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
    
    # Priority queue: (earliest_arrival, total_cost, current_stop, current_line)
    priority_queue = [(start_total, 0, starting_stop, None)]
    heapq.heapify(priority_queue)
    
    while priority_queue:
        current_time, current_cost, current_stop, current_line = heapq.heappop(priority_queue)
        
        # Skip if we've already found a better path to this node
        if current_time > earliest_arrival[current_stop]:
            continue
        
        # ?
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
            if criteria == 't':  # Time-optimized
                total_edge_cost = neighbor_edge.travel_time + wait_time
            elif criteria == 'p':  # Transfer-optimized
                total_edge_cost = (100 if (current_line and neighbor_edge.line != current_line) else 0) + wait_time + neighbor_edge.travel_time
            
            #total_edge_cost = neighbor_edge.travel_time + wait_time + transfer_penalty
            new_cost = current_cost + total_edge_cost
            
            
            if new_cost < distance[neighbor_edge.end]:
                distance[neighbor_edge.end] = new_cost
                earliest_arrival[neighbor_edge.end] = arr_total
                previous[neighbor_edge.end] = (current_stop, neighbor_edge, neighbor_edge.line)
                heapq.heappush(priority_queue, (arr_total, new_cost, neighbor_edge.end, neighbor_edge.line))
                
    stop_algorithm_time = datetime.now()
    log(f"Dijkstra execution time: {stop_algorithm_time - start_algorithm_time} seconds")
    
    path, final_arrival_time = reconstruct_path(previous, starting_stop, destination_stop)
    if path is None:
        print("Error reconstructing path")
        return None, None
    
    total_travel_time = calculate_total_travel_time(start_total, final_arrival_time)
    print_path(path, starting_stop_name, start_time, total_travel_time)
    
    return path, total_travel_time




def new_find_dijkstra_path(graph, starting_stop_name, destination_stop_name, start_time, criteria):
    start_algorithm_time = datetime.now()
    starting_stop = graph.get_node(starting_stop_name)
    destination_stop = graph.get_node(destination_stop_name)
    
    if not starting_stop or not destination_stop:
        print("Error: Invalid start or destination stop")
        return None, None
    
    start_total = time_to_minutes(start_time)
    
    # distance = {}
    # previous = {}
    # transfers = {} #change this and the queue to sart with current time
    # for node in graph.get_nodes():
    #     distance[node] = float('inf')
    #     previous[node] = (None, None, None)
    #     transfers[node] = float('inf')
    # distance[starting_stop] = 0
    # transfers[starting_stop] = 0
    distance = {node: float('inf') for node in graph.get_nodes()}
    previous = {node: (None, None, None) for node in graph.get_nodes()}
    earliest_arrival = {node: float('inf') for node in graph.get_nodes()}
    
    distance[starting_stop] = 0
    earliest_arrival[starting_stop] = start_total
    
    # Priority queue: (earliest_arrival, total_cost, current_stop, current_line)
    priority_queue = [(start_total, 0, starting_stop, None)]
    heapq.heapify(priority_queue)
    
    while priority_queue:
        # current_transfers, current_cost, current_stop, current_line, current_time = heapq.heappop(priority_queue)
        current_time, current_cost, current_stop, current_line = heapq.heappop(priority_queue)
        
        # Skip if we've already found a better path to this node
        if current_time > earliest_arrival[current_stop]:
            continue
        
        # ?
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
            # new_transfer_count = current_transfers + (1 if (current_line is not None and neighbor_edge.line != current_line) else 0)
            # transfer_penalty = 20 if (current_line is not None and neighbor_edge.line != current_line) else 0
            
            if criteria == 't':  # Time-optimized
                total_edge_cost = neighbor_edge.travel_time + wait_time
            elif criteria == 'p':  # Transfer-optimized
                total_edge_cost = (100 if (current_line and neighbor_edge.line != current_line) else 0)+ wait_time + neighbor_edge.travel_time
            
            #total_edge_cost = neighbor_edge.travel_time + wait_time + transfer_penalty
            new_cost = current_cost + total_edge_cost
            
            
            if new_cost < distance[neighbor_edge.end]:
                distance[neighbor_edge.end] = new_cost
                earliest_arrival[neighbor_edge.end] = arr_total
                # transfers[neighbor_edge.end] = new_transfer_count
                previous[neighbor_edge.end] = (current_stop, neighbor_edge, neighbor_edge.line)
                heapq.heappush(priority_queue, (arr_total, new_cost, neighbor_edge.end, neighbor_edge.line))
                
    stop_algorithm_time = datetime.now()
    log(f"Dijkstra execution time: {stop_algorithm_time - start_algorithm_time} seconds")
    
    
    path, final_arrival_time = reconstruct_path(previous, starting_stop, destination_stop)
    if path is None:
        print("Error reconstructing path")
        return None, None
    
    total_travel_time = calculate_total_travel_time(start_total, final_arrival_time)
    print_path(path, starting_stop_name, start_time, total_travel_time)
    
    return path, total_travel_time








#CURRENT BEST VERSION but trying to modify
def stable_find_dijkstra_path(graph, starting_stop_name, destination_stop_name, start_time, criteria):
    start_algorithm_time = datetime.now()
    starting_stop = graph.get_node(starting_stop_name)
    destination_stop = graph.get_node(destination_stop_name)
    
    if starting_stop is None or destination_stop is None:
        print("Starting stop not found")
        return
    
    start_total = time_to_minutes(start_time)
    
    distance = {}
    previous = {}
    transfers = {} #change this and the queue to sart with current time
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
    
    
    path, final_arrival_time = reconstruct_path(previous, starting_stop, destination_stop)
    if path is None:
        print("Error reconstructing path")
        return None, None
    
    total_travel_time = calculate_total_travel_time(start_total, final_arrival_time)
    print_path(path, starting_stop_name, start_time, total_travel_time)
    
    return path, total_travel_time