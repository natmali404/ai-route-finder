import random
from graph import Graph, Node, Edge
from utils import get_graph, print_path
from dijkstra_algorithm import find_dijkstra_path
from a_algorithm import find_a_star_path
from tabu_search import tabu_search

#debug 1
def print_random_nodes_with_edges(graph, num_nodes=10):
    if len(graph.nodes) < num_nodes:
        print(f"Graph has fewer than {num_nodes} nodes. Printing all nodes instead.")
        num_nodes = len(graph.nodes)
    
    random_nodes = random.sample(graph.nodes, num_nodes)
    
    for node in random_nodes:
        print(f"\nNode: {node}")
        print(f"Outgoing edges from {node.name}:")
        for edge in node.get_outgoing_edges():
            print(f"  - {edge}")
            
#debug 2
def print_edges_of_node(graph, nodename):
    node = graph.get_node(nodename)
    print(f"\nNode: {node}")
    print(f"Outgoing edges from {node.name}:")
    for edge in node.get_outgoing_edges():
        print(f"  - {edge}")
   


#if __name__ == "__main__":
    #print("Begin graph initialization...")
    #graph = get_graph()
    #print(f"Graph has {len(graph.nodes)} nodes and {len(graph.edges)} edges.")
    # for edge in graph.edges:
    #     if edge.start == "most Grunwaldzki" and edge.end == "PL. GRUNWALDZKI":
    #         print(edge)
    
    #tests
    #find_dijkstra_path(graph, "PL. GRUNWALDZKI", "Wrocławski Park Przemysłowy", "15:49")
    # find_dijkstra_path(graph, "Stalowa", "PL. GRUNWALDZKI", "15:49")
    # find_dijkstra_path(graph, "PL. GRUNWALDZKI", "Wrocławski Park Przemysłowy", "15:51")
    # find_dijkstra_path(graph, "Stalowa", "PL. GRUNWALDZKI", "15:51")
    #find_dijkstra_path(graph, "Kątna", "Klęka", "12:00")
    #find_dijkstra_path(graph, "Mokra", "Lekarska", "12:00")
    #find_dijkstra_path(graph, "Przejazdowa", "PL. GRUNWALDZKI", "12:00")
    # find_a_star_path(graph, "PL. GRUNWALDZKI", "Wrocławski Park Przemysłowy", "15:49", 'euclidean')
    
    
    # path, total_travel_time, _ = find_a_star_path(graph, "PL. GRUNWALDZKI", "Wrocławski Park Przemysłowy", "15:49", 'manhattan')
    # print_path(path, "PL. GRUNWALDZKI", "15:49", total_travel_time)
    # path, total_travel_time, _ = find_a_star_path(graph, "Kątna", "Klęka", "12:00", 'euclidean')
    # print_path(path, "Kątna", "12:00", total_travel_time)
    
    
    #find_a_star_path(graph, "Kątna", "Klęka", "12:00", 'manhattan')
    #find_tabu_search_path(graph, "PL. GRUNWALDZKI", ['Wrocławski Park Przemysłowy', 'Arkady (Capitol)', 'pl. Wróblewskiego'], '12:00', 't')
    
    #solution = tabu_search(graph, "PL. GRUNWALDZKI", ['Wrocławski Park Przemysłowy', 'Arkady (Capitol)', 'pl. Wróblewskiego'], '12:00', 't')
    # solution format: (stop_list, total_cost, path)
    # print(f'Solution found: {solution[0]}, cost: {solution[1]}')
    # print(f'Path: {solution[2]}')
    # print_path(solution[2], "PL. GRUNWALDZKI", "12:00")
    


def get_user_input():
    print("Choose an algorithm:")
    print("1. Dijkstra")
    print("2. A*")
    print("3. Tabu Search")
    print("4. debug")
    
    choice = input("Enter the number of the algorithm: ").strip()
    
    if choice in ['1', '2']:
        start_stop = input("Enter the start stop: ").strip()
        end_stop = input("Enter the end stop: ").strip()
        start_time = input("Enter the start time (HH:MM): ").strip()
        criteria = input("Enter criteria (t for time, p for preference): ").strip()
        
        if choice == '2':  # A*
            heuristic = input("Enter heuristic (euclidean, manhattan, haversine): ").strip()
            return choice, start_stop, end_stop, start_time, criteria, heuristic
        
        return choice, start_stop, end_stop, start_time, criteria
    elif choice == '3':
        start_stop = input("Enter the start stop: ").strip()
        stop_list = input("Enter a list of stops separated by semicolons: ").strip().split(';')
        start_time = input("Enter the start time (HH:MM): ").strip()
        criteria = input("Enter criteria (t for time, p for preference): ").strip()
        
        return choice, start_stop, stop_list, start_time, criteria
    else:
        return choice, None, None, None, None, None
    # else:
    #     print("Invalid choice. Please restart the program and choose a valid option.")
    #     exit()

def main():
    print("Initializing graph...")
    graph = get_graph()
    print(f"Graph loaded with {len(graph.nodes)} nodes and {len(graph.edges)} edges.")
    
    user_input = get_user_input()
    
    if user_input[0] == '1':  # Dijkstra
        path, total_time = find_dijkstra_path(graph, user_input[1], user_input[2], user_input[3], user_input[4])
        print(f"Dijkstra Path: {path}, Total time: {total_time}")
        print_path(path, user_input[1], user_input[3], total_time)
    
    elif user_input[0] == '2':  # A*
        path, total_time, _ = find_a_star_path(graph, user_input[1], user_input[2], user_input[3], user_input[4], user_input[5])
        print(f"A* Path: {path}, Total time: {total_time}")
        print_path(path, user_input[1], user_input[3], total_time)
    
    elif user_input[0] == '3':  # Tabu Search
        solution = tabu_search(graph, user_input[1], user_input[2], user_input[3], user_input[4])
        print(f"Tabu Search Solution: {solution[0]}, Cost: {solution[1]}")
        print(f"Path: {solution[2]}")
        print_path(solution[2], user_input[1], user_input[3])
        
    else:
        # path, total_time = find_dijkstra_path(graph, "PL. GRUNWALDZKI", "Wrocławski Park Przemysłowy", "14:40", 'p')
        # path, total_time = find_dijkstra_path(graph, "most Grunwaldzki", "Wrocławski Park Przemysłowy", "14:41", 'p')
        path, total_time = find_dijkstra_path(graph, "PL. GRUNWALDZKI", "Wrocławski Park Przemysłowy", "14:40", 't')
        print(f"Dijkstra Path: {path}, Total time: {total_time}")
        #print_path(path, "PL. GRUNWALDZKI", "14:40", total_time)
        print_path(path, "PL. GRUNWALDZKI", "14:40", total_time)
        path, total_time = find_dijkstra_path(graph, "PL. GRUNWALDZKI", "Wrocławski Park Przemysłowy", "14:40", 'p')
        print_path(path, "PL. GRUNWALDZKI", "14:40", total_time)
    

if __name__ == "__main__":
    main()
