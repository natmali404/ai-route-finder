import heapq
import pandas as pd
from datetime import datetime, timedelta

def transit_dijkstra(graph, start_stop, end_stop, start_time):
    """
    Implementation of Dijkstra's algorithm for transit networks that considers:
    - Time-dependent connections
    - Waiting times
    - Line changes
    
    Args:
        graph: NetworkX MultiDiGraph with transit connections
        start_stop: String name of the starting bus/tram stop
        end_stop: String name of the destination stop
        start_time: String time in format "HH:MM" or "HH:MM:SS"
    
    Returns:
        path: List of tuples (stop, line, time) representing the path
        total_cost: Total travel time in minutes
    """
    # Validate input stops
    if not graph.has_node(start_stop) or not graph.has_node(end_stop):
        raise ValueError(f"Stop '{start_stop}' or '{end_stop}' does not exist in the graph.")
    
    # Ensure start_time is in datetime format
    if isinstance(start_time, str):
        # Handle both HH:MM and HH:MM:SS formats
        if len(start_time.split(':')) == 2:
            start_time = pd.to_datetime(start_time + ":00")
        else:
            start_time = pd.to_datetime(start_time)
    
    # Initialize data structures
    costs = {node: float('inf') for node in graph.nodes()}
    costs[start_stop] = 0
    previous = {node: None for node in graph.nodes()}
    
    # Priority queue: (cost, stop, current_time, current_line)
    # Adding current_line to track line changes
    priority_queue = [(0, start_stop, start_time, None)]
    
    # To avoid revisiting nodes with worse paths
    visited = set()
    
    while priority_queue:
        current_cost, current_stop, current_time, current_line = heapq.heappop(priority_queue)
        
        # If we've already found a better path to this stop
        current_key = (current_stop, current_line)
        if current_key in visited:
            continue
        
        # If we've reached our destination
        if current_stop == end_stop:
            break
        
        # Mark as visited
        visited.add(current_key)
        
        # Explore all neighbors
        for neighbor in graph.successors(current_stop):
            # Get all edges between current_stop and neighbor
            edges = graph.get_edge_data(current_stop, neighbor)
            
            # Find the best connection to this neighbor
            best_cost = float('inf')
            best_data = None
            
            for edge_id, data in edges.items():
                # Parse departure time
                dep_time = pd.to_datetime(data['dep_time'])
                
                # Skip connections that have already departed
                if dep_time < current_time:
                    continue
                
                # Calculate wait time
                wait_time = (dep_time - current_time).total_seconds() / 60
                
                # Calculate travel time
                travel_time = data['weight']
                
                # Add line change penalty if changing lines
                line_change_penalty = 0
                if current_line is not None and current_line != data['line']:
                    line_change_penalty = 3  # Penalty for changing lines (can be adjusted)
                
                # Calculate total cost for this connection
                new_cost = current_cost + travel_time + wait_time + line_change_penalty
                
                # If this is the best connection so far
                if new_cost < best_cost:
                    best_cost = new_cost
                    # Save arrival time and line information
                    arr_time = pd.to_datetime(data['arr_time'])
                    best_data = (arr_time, data['line'], dep_time)
            
            # If we found a better path to this neighbor
            if best_data and best_cost < costs[neighbor]:
                costs[neighbor] = best_cost
                # Store previous stop, line used, and departure time
                previous[neighbor] = (current_stop, best_data[1], best_data[2])
                # Add to priority queue with the new line
                heapq.heappush(priority_queue, (best_cost, neighbor, best_data[0], best_data[1]))
    
    # Reconstruct path
    path = []
    current = end_stop
    
    while current:
        prev_data = previous[current]
        if prev_data:
            # Add (stop, line, departure_time)
            path.append((current, prev_data[1], prev_data[2]))
            current = prev_data[0]
        else:
            # Add the starting point without line info
            path.append((current, None, start_time))
            break
    
    # Reverse path to get start->end
    path = path[::-1]
    
    return path, costs[end_stop]

def format_transit_path(path, total_cost):
    """
    Format the path into a readable string
    
    Args:
        path: List of tuples (stop, line, time)
        total_cost: Total cost (time) of the journey
    
    Returns:
        String with formatted journey information
    """
    if not path or len(path) < 2:
        return "No valid path found."
    
    result = []
    result.append(f"Journey from {path[0][0]} to {path[-1][0]}")
    result.append(f"Departure time: {path[0][2].strftime('%H:%M:%S')}")
    result.append(f"Arrival time: {path[-1][2].strftime('%H:%M:%S')}")
    result.append(f"Total travel time: {int(total_cost)} minutes")
    result.append("")
    
    # Group segments by line
    current_line = None
    line_segments = []
    
    for i in range(1, len(path)):
        stop, line, time = path[i]
        prev_stop, prev_line, prev_time = path[i-1]
        
        if line != current_line:
            # Output the previous line's segments
            if line_segments:
                first_seg = line_segments[0]
                last_seg = line_segments[-1]
                result.append(f"Take line {current_line} from {first_seg[0]} to {last_seg[1]}")
                
                for from_stop, to_stop, dep_time, arr_time in line_segments:
                    result.append(f"  {from_stop} → {to_stop} ({dep_time.strftime('%H:%M')} - {arr_time.strftime('%H:%M')})")
                
                result.append("")
            
            # Start a new line segment
            current_line = line
            line_segments = [(prev_stop, stop, prev_time, time)]
        else:
            # Continue the current line
            line_segments.append((prev_stop, stop, prev_time, time))
    
    # Don't forget the last line segment
    if line_segments:
        first_seg = line_segments[0]
        last_seg = line_segments[-1]
        result.append(f"Take line {current_line} from {first_seg[0]} to {last_seg[1]}")
        
        for from_stop, to_stop, dep_time, arr_time in line_segments:
            result.append(f"  {from_stop} → {to_stop} ({dep_time.strftime('%H:%M')} - {arr_time.strftime('%H:%M')})")
    
    # Count line changes
    line_changes = len([i for i in range(1, len(path)) if path[i][1] != path[i-1][1] and path[i-1][1] is not None]) 
    result.append(f"\nNumber of line changes: {line_changes}")
    
    return "\n".join(result)

def find_route(G, start_stop, end_stop, start_time):
    """Find and display the shortest route between two stops"""
    try:
        path, total_cost = transit_dijkstra(G, start_stop, end_stop, start_time)
        print(format_transit_path(path, total_cost))
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")