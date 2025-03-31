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
   


if __name__ == "__main__":
    print("Begin graph initialization...")
    graph = get_graph()
    print(f"Graph has {len(graph.nodes)} nodes and {len(graph.edges)} edges.")
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
    
    solution = tabu_search(graph, "PL. GRUNWALDZKI", ['Wrocławski Park Przemysłowy', 'Arkady (Capitol)', 'pl. Wróblewskiego'], '12:00', 't')
    # solution format: (stop_list, total_cost, path)
    print(f'Solution found: {solution[0]}, cost: {solution[1]}')
    print(f'Path: {solution[2]}')
    print_path(solution[2], "PL. GRUNWALDZKI", "12:00")