import math
from utils import minutes_to_time, time_to_minutes, print_path, log, reconstruct_path, calculate_total_travel_time
from a_algorithm import find_a_star_path


def generate_neighbourhood(stop_list, tabu_list):
    neighbourhood = []
    
    for i in range(len(stop_list)):
        for j in range(i + 1, len(stop_list)):
            new_stop_list = stop_list.copy()
            new_stop_list[i], new_stop_list[j] = new_stop_list[j], new_stop_list[i]  # swap
            
            if tuple(new_stop_list) not in tabu_list:
                neighbourhood.append(new_stop_list)
    
    return neighbourhood


def calculate_cost(graph, starting_stop, stop_list, start_time, optimalization_criteria):
    stop_list = [starting_stop] + stop_list + [starting_stop]  #include start/end stop
    total_cost = 0
    total_path = []
    current_start_time = start_time

    for i in range(len(stop_list) - 1):
        path, total_travel_time, route_cost = find_a_star_path(graph, stop_list[i], stop_list[i + 1], current_start_time, optimalization_criteria, 'manhattan')
        current_start_time = minutes_to_time(time_to_minutes(current_start_time) + total_travel_time)
        total_cost += route_cost
        total_path += path

    return total_cost, total_path

#DOCUMENT THIS
#fix a star finding inconsistent times/solutions
def tabu_search(graph, starting_stop, stop_list, start_time, optimalization_criteria):
    current_best_solution = (stop_list, float('inf'), [])
    tabu_list = []
    best_solution = current_best_solution
    
    max_tabu_size = max(7, len(stop_list))  #prevent large factorial growth
    max_iterations = 100
    iteration = 0
    
    while len(tabu_list) < max_tabu_size and iteration < max_iterations:
        neighbourhood = generate_neighbourhood(current_best_solution[0], tabu_list)
        
        if not neighbourhood:  #stop if no new valid swaps exist
            break
        
        costs = {}
        for new_solution in neighbourhood:
            total_cost, total_path = calculate_cost(graph, starting_stop, new_solution, start_time, optimalization_criteria)
            costs[tuple(new_solution)] = [total_cost, total_path]  #store as tuple for performance
        
        best_neighbour = min(costs, key=lambda x: costs[x][0])
        best_neighbour_cost = costs[best_neighbour][0]
        best_neighbour_path = costs[best_neighbour][1]

        current_best_solution = (list(best_neighbour), best_neighbour_cost, best_neighbour_path)

        #fifo
        tabu_list.append(best_neighbour)
        if len(tabu_list) > max_tabu_size:
            tabu_list.pop(0)

        if current_best_solution[1] < best_solution[1]:
            best_solution = current_best_solution
        
        iteration += 1

    return best_solution
