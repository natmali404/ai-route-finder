import sys
import csv
import time
import random
from datetime import datetime
from collections import defaultdict
import networkx as nx
import matplotlib.pyplot as plt
from dijkstra_algorithm import dijkstra_search, optimized_dijkstra, simplified_dijkstra
from new_code import find_route

#algorytm wyszukiwania najkrótszych połączeń pomiędzy zadanymi przystankami A i B
#miarę odległości, zależnie od decyzji użytkownika, czas dojazdu z A do B lub liczba przesiadek koniecznych do wykonania

#input:
#przystanek start A
#przystanek end B
#kryt. opt.: wartość t oznacza minimalizację czasu dojazdu, wartość p oznacza minimalizację liczby zmian linii
#czas pojawienia się na przystanku początkowym

            
#sys.stdout.write("To jest stdout\n")
#sys.stdout.write("To jest stderr\n")

#stdout:
#harmonogram przejazdu, wypisując w kolejnych liniach informacje o kolejno wykorzystanych liniach komunikacyjnych (nazwa linii, czas i przystanek, na którym wsiadamy do danej linii komunikacyjnej oraz czas i przystanek,
#na którym kończymy korzystać z danej linii). 

#stderr:
#wartość funkcji kosztu znalezionego rozwiązania oraz czas obliczeń liczony od wczytania danych do uzyskania rozwiązania.

def format_time(timestamp):
    return timestamp.strftime("%Y-%m-%d %H:%M:%S.%f")[:-4]

#format: ['4136', 'MPK Autobusy', 'A', '05:18:00', '05:19:00', 'FAT', 'GRABISZYŃSKA (Cmentarz)', '51.09412632', '16.9783528', '51.08990377', '16.97664203']

def get_graph():
    G = nx.MultiDiGraph()

    unique_edges = set()

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

                if start not in G: #do i have to check that?
                    G.add_node(start, lat=start_stop_lat, lon=start_stop_lon)
                if end not in G:
                    G.add_node(end, lat=end_stop_lat, lon=end_stop_lon)

                dep_h, dep_m, dep_s = map(int, dep_time.split(":"))
                arr_h, arr_m, arr_s = map(int, arr_time.split(":"))
                dep_mins = dep_h * 60 + dep_m
                arr_mins = arr_h * 60 + arr_m
                travel_time = abs(arr_mins - dep_mins)
                
                if dep_h >= 24:
                    dep_time = f"{(dep_h-24):02d}:{(dep_m):02d}:00"
                
                if arr_h >= 24:
                    arr_time = f"{(arr_h-24):02d}:{(arr_m):02d}:00"

                edge_identifier = (start, end, line, dep_time, arr_time, travel_time)
                unique_edges.add(edge_identifier)

            except Exception as e:
                print(f"Error in line {data_row}: {e}")

        for start, end, line, dep_time, arr_time, travel_time in unique_edges:
            G.add_edge(start, end, line=line, dep_time=dep_time, arr_time=arr_time, weight=travel_time)

    return G


#debug
def print_random_nodes(graph, count=20):
    nodes = list(graph.nodes(data=True))
    sample_nodes = random.sample(nodes, min(count, len(nodes)))
    print("\n🔹 Losowe węzły (pełna struktura):")
    for node, attrs in sample_nodes:
        print(f"{node}: {attrs}")

def print_random_edges(graph, count=20):
    edges = list(graph.edges(data=True, keys=True))
    sample_edges = random.sample(edges, min(count, len(edges)))
    print("\n🔹 Losowe krawędzie (pełna struktura):")
    for u, v, key, attrs in sample_edges:
        print(f"{u} -> {v} [{key}]: {attrs}")



def draw_graph(G, bus_stop_list):
    print(f"Plotting for {bus_stop_list}")
    print("Setting size")
    plt.figure(figsize=(12, 10))

    print("Creating the pos dictionary")
    pos = {node: (data["lon"], data["lat"]) for node, data in G.nodes(data=True)}

    edges_to_plot = [(u, v) for u, v in G.edges() if u in bus_stop_list and v in bus_stop_list]
    nodes_to_plot = set([node for edge in edges_to_plot for node in edge])

    nx.draw(
        G, 
        pos, 
        with_labels=True, 
        node_size=50, 
        node_color="lightblue", 
        edge_color="gray", 
        font_size=6, 
        edgelist=edges_to_plot,
        nodelist=nodes_to_plot
    )

    print("Adding edge labels")
    edge_labels = {(u, v): G[u][v].get("weight", "") for u, v in edges_to_plot}

    if len(edge_labels) > 1000:
        edge_labels = {key: edge_labels[key] for i, key in enumerate(edge_labels) if i < 1000}

    nx.draw_networkx_edge_labels(
        G, 
        pos, 
        edge_labels=edge_labels, 
        font_size=5, 
        font_color="red"
    )

    plt.title("Graf połączeń komunikacyjnych (geograficzny)", fontsize=16)
    plt.xlabel("Długość geograficzna")
    plt.ylabel("Szerokość geograficzna")

    plt.show()




def print_edges(graph, stop_name, filename="edges_output.txt"):
    with open(filename, 'w', encoding='utf-8') as f:
        outgoing_edges = graph.out_edges(stop_name, data=True, keys=True)
        f.write(f"\nOutgoing edges - {stop_name}:\n")
        for u, v, key, attrs in outgoing_edges:
            f.write(f"{u} -> {v} [{key}]: {attrs}\n")

        incoming_edges = graph.in_edges(stop_name, data=True, keys=True)
        f.write(f"\nIncoming edges - {stop_name}:\n")
        for u, v, key, attrs in incoming_edges:
            f.write(f"{u} <- {v} [{key}]: {attrs}\n")

    print(f"Edges have been written to {filename}")



if __name__ == "__main__":
    print(f"{format_time(datetime.now())} - Begin building graph")
    G = get_graph()
    print(f"{format_time(datetime.now())} - Finished building graph")

    #print_edges(G, "PL. GRUNWALDZKI")
    bus_stop_list = ["PL. GRUNWALDZKI", "Most Grunwaldzki", "Urząd Wojewódzki (Impart)", "Reja", "Kliniki - Politechnika Wrocławska"]
    #draw_graph(G, bus_stop_list)
    print_random_nodes(G)
    print_random_edges(G)

    # print(f"{format_time(datetime.now())} - Begin Dijkstra")
    # dijkstra_search(G, "PL. GRUNWALDZKI", "Wrocławski Park Przemysłowy", "18:47")
    # print(f"{format_time(datetime.now())} - Finish Dijkstra")
    # print(f"{format_time(datetime.now())} - Begin Optimized Dijkstra")
    # optimized_dijkstra(G, "PL. GRUNWALDZKI", "Wrocławski Park Przemysłowy", "18:47")
    # print(f"{format_time(datetime.now())} - Finished Optimized Dijkstra")
    print(f"{format_time(datetime.now())} - Begin Simplified Dijkstra")
    path, cost = simplified_dijkstra(G, "PL. GRUNWALDZKI", "Wrocławski Park Przemysłowy", "23:49")
    print("Shortest path:")
    for stop in path:
        if stop[1]:
            print(f"{stop[0]} - line {stop[1]} ({stop[2]} - {stop[3]})")
    print(f"Total travel time: {cost} minutes")
    print(f"{format_time(datetime.now())} - Finished Simplified Dijkstra")
    # print(f"{format_time(datetime.now())} - Begin New Dijkstra")
    # find_route(G, "PL. GRUNWALDZKI", "Wrocławski Park Przemysłowy", "18:47")
    # print(f"{format_time(datetime.now())} - Finished New Dijkstra")
