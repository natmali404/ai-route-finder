#algorytm wyszukiwania najkrótszej ścieżki z A do B za pomocą algorytmu algorytmem Dijkstry w oparciu o kryterium czasu (10 punktów)

# 1 budowanie grafu

# wierzcholki to przystanki
# krawedzie to przejazdy: linia, czas przejazdu itp

def dijkstra_search(start_stop, end_stop, arrival_time):
    print(f"Dijkstra search: \n {arrival_time}: {start_stop}->{end_stop}")
    
    #find the start stop
    #get all routes starting at the nearest time to arrival_time
    #begin dijkstra search
