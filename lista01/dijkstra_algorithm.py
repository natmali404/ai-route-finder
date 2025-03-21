import networkx as nx
import heapq
import pandas as pd
#algorytm wyszukiwania najkrótszej ścieżki z A do B za pomocą algorytmu algorytmem Dijkstry w oparciu o kryterium czasu (10 punktów)

# 1 budowanie grafu

# wierzcholki to przystanki
# krawedzie to przejazdy: linia, czas przejazdu itp

# https://www.youtube.com/watch?v=IG1QioWSXRI
def dijkstra_search(graph, start_stop, end_stop, arrival_time):
    print(f"Dijkstra search: \n {arrival_time}: {start_stop}->{end_stop}")
    
    #find the start stop
    if not graph.has_node(start_stop):
        raise ValueError(f"Stop '{start_stop}' does not exist.")
    if not graph.has_node(end_stop):
        raise ValueError(f"Stop '{end_stop}' does not exist.")
    
    shortest_distance = {}
    allNodes = graph.nodes
    path = []
    
    # for neighbor in graph.successors(start_stop):
    
    #jesli mamy kilka tras o takich samych czasach, priorytet ma zawsze ta sama linia
        
    costs = {node: float('inf') for node in graph.nodes()}
    costs[start_stop] = 0
    previous = {node: None for node in graph.nodes()} #prev node on the shortest path
    
    priority_queue = []
    heapq.heappush(priority_queue, (0, start_stop, arrival_time))
    
    
    while priority_queue:
        
        current_cost, current_stop, current_time = heapq.heappop(priority_queue)
        
        if current_stop == end_stop:
            break
        
        for neighbor in graph.successors(current_stop):
            edge_data = graph.get_edge_data(current_stop, neighbor)

            # Znalezienie najwcześniejszego dostępnego połączenia
            best_option = None
            for key, data in edge_data.items():
                dep_time = pd.to_datetime(data['dep_time'])
                arr_time = pd.to_datetime(data['arr_time'])
                weight = data['weight']
                line = data['line']

                # Jeśli odjazd jest późniejszy niż obecny czas podróży
                if dep_time >= pd.to_datetime(current_time):
                    wait_time = (dep_time - pd.to_datetime(current_time)).total_seconds() / 60  # W minutach
                    new_cost = current_cost + weight + wait_time  # Dodanie czasu oczekiwania

                    if best_option is None or new_cost < best_option[0]:
                        best_option = (new_cost, neighbor, arr_time, line, dep_time)

            # Jeśli znaleziono najlepszą opcję dla danego przystanku, aktualizujemy koszt
            if best_option:
                new_cost, neighbor, arr_time, line, dep_time = best_option
                if new_cost < costs[neighbor]:
                    #print(f"New shortest found for {neighbor}: {current_stop}, {line}, {dep_time}")
                    costs[neighbor] = new_cost
                    previous[neighbor] = (current_stop, line, dep_time) #dep time??
                    heapq.heappush(priority_queue, (new_cost, neighbor, arr_time))
                        
    #path reconstruct
    path = []
    current = end_stop
    while current is not None:
        if previous[current] is not None:  # Sprawdź, czy previous[current] nie jest None
            path.append((current, previous[current][1], previous[current][2]))  # (przystanek, linia, czas odjazdu)
        else:
            path.append((current, None, None))  # Dla przystanku początkowego
        current = previous[current][0] if previous[current] else None
    path.reverse()
    
    print("Najkrótsza ścieżka:")
    for stop in path:
        if stop[1]:  # Pomijaj None dla przystanku początkowego
            print(f"{stop[0]} - linia {stop[1]} o godz. {stop[2]}")
    print(f"Całkowity czas podróży: {costs[end_stop]} minut")
    #get all routes starting at the nearest time to arrival_time
    
    #begin dijkstra search


    #funkcja kosztu


def optimized_dijkstra(graph, start_stop, end_stop, arrival_time):
    print(f"Optimized Dijkstra search: {arrival_time}: {start_stop}->{end_stop}")
    
    # Validate input
    if not graph.has_node(start_stop) or not graph.has_node(end_stop):
        raise ValueError(f"Stop '{start_stop}' or '{end_stop}' does not exist.")
    
    # Initial data structures
    costs = {node: float('inf') for node in graph.nodes()}
    costs[start_stop] = 0
    previous = {node: None for node in graph.nodes()}
    
    # Use a dictionary to track nodes in queue for efficient updates
    in_queue = {start_stop: 0}
    visited = set()
    
    # Priority queue with (cost, node_id, time)
    priority_queue = [(0, start_stop, pd.to_datetime(arrival_time))]
    
    while priority_queue:
        current_cost, current_stop, current_time = heapq.heappop(priority_queue)
        
        # If this entry is outdated (we found a better path already), skip it
        if current_cost > in_queue.get(current_stop, float('inf')):
            continue
            
        # Remove from tracking as we're processing it now
        in_queue.pop(current_stop, None)
        
        # If we reached destination, we're done
        if current_stop == end_stop:
            break
        
        # Mark as visited to avoid reprocessing
        visited.add(current_stop)
        
        # Process all neighbors
        for neighbor in graph.successors(current_stop):
            if neighbor in visited:
                continue
                
            edge_data = graph.get_edge_data(current_stop, neighbor)
            best_connection = None
            best_cost = float('inf')
            
            # Find the earliest valid connection
            for _, data in edge_data.items():
                dep_time = pd.to_datetime(data['dep_time'])
                arr_time = pd.to_datetime(data['arr_time'])
                travel_time = data['weight']
                line = data['line']
                
                # Skip connections that leave before we arrive
                if dep_time < current_time:
                    continue
                    
                # Calculate total cost including waiting time
                wait_time = (dep_time - current_time).total_seconds() / 60
                new_cost = current_cost + travel_time + wait_time
                
                # Keep track of the best connection
                if new_cost < best_cost:
                    best_cost = new_cost
                    best_connection = (neighbor, arr_time, line, dep_time)
            
            # If we found a valid connection and it's better than what we had
            if best_connection and best_cost < costs[neighbor]:
                neighbor, arr_time, line, dep_time = best_connection
                costs[neighbor] = best_cost
                previous[neighbor] = (current_stop, line, dep_time)
                
                # Add to queue if not already there, or update if better
                in_queue[neighbor] = best_cost
                heapq.heappush(priority_queue, (best_cost, neighbor, arr_time))
    
    # Path reconstruction (same as before)
    path = []
    current = end_stop
    while current is not None:
        if previous[current] is not None:
            path.append((current, previous[current][1], previous[current][2]))
        else:
            path.append((current, None, None))
        current = previous[current][0] if previous[current] else None
    path.reverse()
    
    # Print results
    print("Shortest path:")
    for stop in path:
        if stop[1]:
            print(f"{stop[0]} - line {stop[1]} at {stop[2]}")
    print(f"Total travel time: {costs[end_stop]} minutes")
    
    return path, costs[end_stop]


def simplified_dijkstra(graph, start_stop, end_stop, arrival_time):
    if not graph.has_node(start_stop) or not graph.has_node(end_stop):
        raise ValueError(f"Stop '{start_stop}' or '{end_stop}' does not exist.")
    
    costs = {node: float('inf') for node in graph.nodes()}
    costs[start_stop] = 0
    previous = {node: None for node in graph.nodes()}
    
    # Single priority queue
    priority_queue = [(0, start_stop, pd.to_datetime(arrival_time))]
    visited = set()
    
    while priority_queue:
        current_cost, current_stop, current_time = heapq.heappop(priority_queue)
        
        if current_stop in visited:
            continue
            
        if current_stop == end_stop:
            break
            
        visited.add(current_stop)
        
        for neighbor in graph.successors(current_stop):
            if neighbor in visited:
                continue
                
            best_cost = float('inf')
            best_data = None
            
            for _, data in graph.get_edge_data(current_stop, neighbor).items():
                dep_time = pd.to_datetime(data['dep_time'])
                
                if dep_time < current_time:
                    continue
                    
                wait_time = (dep_time - current_time).total_seconds() / 60
                new_cost = current_cost + data['weight'] + wait_time
                
                if new_cost < best_cost:
                    best_cost = new_cost
                    best_data = (data['arr_time'], data['line'], dep_time, data['arr_time'])
            
            if best_data and best_cost < costs[neighbor]:
                costs[neighbor] = best_cost
                previous[neighbor] = (current_stop, best_data[1], best_data[2], best_data[3])
                heapq.heappush(priority_queue, (best_cost, neighbor, pd.to_datetime(best_data[0])))
    
    # Simplified path reconstruction
    path = []
    current = end_stop
    while current:
        prev_data = previous[current]
        path.append((current, None if not prev_data else prev_data[1], 
                    None if not prev_data else prev_data[2], None if not prev_data else prev_data[3]))
        current = None if not prev_data else prev_data[0]
    
    return path[::-1], costs[end_stop]

