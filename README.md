# Algorytmy przeszukiwania Dijkstra, A*. Lokalne przeszukiwanie i Tabu Search

##  Użyte biblioteki
W zadaniu wykorzystane zostały następujące standardowe biblioteki Pythona:

```
math
datetime
os
json
csv
bisect
random
heapq
```

# Struktury danych

W zadaniu wykorzystana została autorska struktura grafu, znajdująca się w pliku `graph.py`. Za jej pomocą modelowane są dane z dostarczonego pliku csv.

## Node
Każdy węzeł ma następujące atrybuty:
- `name` – unikalna nazwa węzła,
- `lat, lon` – współrzędne geograficzne węzła,
- `outgoing_edges` – lista wychodzących krawędzi (posortowana według czasu odjazdu).


## Edge
Każda krawędź reprezentuje połączenie między dwoma węzłami i zawiera:
- `start` – węzeł początkowy,
- `end` – węzeł końcowy,
- `line` – oznaczenie linii (np. numer trasy transportowej),
- `dep_time, arr_time` – czas odjazdu i przyjazdu,
- `travel_time` – czas podróży w minutach,
- `dep_minutes, arr_minutes` – czas odjazdu i przyjazdu przeliczony na minuty od początku dnia.

Potrzebne były również funkcje pomocnicze do zarządzania czasem.


## Graph
Obiekt grafu przechowuje węzły i krawędzie oraz umożliwia:
- Dodawanie nowych węzłów (`add_node`),
- Dodawanie nowych krawędzi (`add_edge`),
- Pobieranie węzła po nazwie (`get_node`),
- Serializację do JSON (`to_json`) oraz deserializację z JSON (`from_json`).


# Funkcje pomocnicze

W zadaniu wykorzystuję szereg funkcji pomocniczych, znajdujących się w pliku `utils.py`. Oto najważniejsze z nich:

## get_graph()

Umożliwia zbudowanie grafu z danych w csv oraz jego serializację do formatu json celem szybszego działania pomiędzy wywołaniami.

## reconstruct_path() oraz print_path()
### format_time(), calculate_total_travel_time() oraz log()
Metody pomocne przy rekonstrukcji ścieżek wyznaczonych przez algorytm oraz ładnym i czytelnym ich sformatowaniu.

## get_user_input() oraz main()

Te metody posłużyły, aby utworzyć CLI dla użytkownika.

# Zadanie 1.

## a) Algorytm Dijkstry

### Opis teoretyczny metody
Algorytm Dijkstry jest jednym z najbardziej znanych algorytmów znajdowania najkrótszej ścieżki w grafie o dodatnich wagach. Działa na zasadzie stopniowego rozszerzania zbioru wierzchołków, dla których najkrótsza ścieżka od węzła początkowego została już znaleziona. Wykorzystuje kolejkę priorytetową do wyboru wierzchołka o najniższym koszcie przejścia.

### Przykładowe zastosowania
nawigacja GPS, transport publiczny, optymalizacja tras dla sieci komputerowych

### Wprowadzone modyfikacje
Poniżej wypisano szereg modyfikacji wprowadzonych do algorytmu. Nie wszystkie z nich okazały się działać poprawnie.
- wprowadzenie kolejki priorytetowej
- śledzenie najwcześniejszego znalezionego czasu dotarcia na przystanek celem optymalizacji czasu wykonywania
- wprowadzenie liniowej kary za przesiadki
- śledzenie ilości przesiadek
- próba priorytetyzowania tej samej linii odjeżdzającej o tej samej godzienie z badanego przystanku
- różne kombinacje wartości w kolejce priorytetowej

### Materiały dodatkowe
- wizualizacja Dijkstry [https://www.cs.usfca.edu/~galles/visualization/Dijkstra.html]
- Dijkstra z kolejką priorytetową [https://www.geeksforgeeks.org/dijkstras-shortest-path-algorithm-using-priority_queue-stl/]
- [https://en.wikipedia.org/wiki/Dijkstra's_algorithm]

### Wykorzystane biblioteki i funkcje pomocnicze
- datetime do mierzenia czasu
- heapq do kolejki priorytetowej
  

## b) Algorytm A*

### Opis teoretyczny metody
Algorytm A* (A-star) to popularny algorytm wyszukiwania ścieżek w grafach, który łączy cechy algorytmu Dijkstry i algorytmu zachłannego przeszukiwania w głąb. Działa na zasadzie minimalizacji funkcji kosztu f(n) = g(n) + h(n), gdzie g to rzeczywisty koszt dojścia ze startu do węzła n, a h to oszacowanie heurystyczne kosztu dojścia z węzła n do celu.

### Przykładowe zastosowania
gry komputerowe, robotyka, automatyzacja, AI

### Wprowadzone modyfikacje
Poniżej wypisano szereg modyfikacji wprowadzonych do algorytmu. Nie wszystkie z nich okazały się działać poprawnie.
- kolejka priorytetowa 
- śledzenie liczby przesiadek oraz wykorzystywanie jej w kolejce priorytetowej
- wprowadzenie heurystyki haversine

### Materiały dodatkowe
- [https://medium.com/@nicholas.w.swift/easy-a-star-pathfinding-7e6689c7f7b2]
- [https://www.redblobgames.com/pathfinding/a-star/introduction.html]

### Wykorzystane biblioteki i funkcje pomocnicze
- datetime do mierzenia czasu
- heapq do kolejki priorytetowej
- math dla heurystyk


## c) Kryteria t/p

Zgodnie z poleceniem wprowadzono kryteria t oraz p celem wyboru priorytetyzowania albo najkrótszego czasu podróży, albo najmniejszej ilości przesiadek.

```python
criteria = 'p' #or 't'

if criteria == 't':
                total_edge_cost = (10 if (current_line and neighbor_edge.line != current_line) else 0) + neighbor_edge.travel_time + wait_time
            elif criteria == 'p':
                total_edge_cost = (100*new_transfer_count if (current_line and neighbor_edge.line != current_line) else 0) + wait_time + neighbor_edge.travel_time
                #or:
                total_edge_cost = (math.pow(15,new_transfer_count) if (current_line and neighbor_edge.line != current_line) else 0) + wait_time + neighbor_edge.travel_time
                
```

## d) Heurystyki

- Euklidesowa - Najkrótsza odległość "po prostej", ignoruje krzywiznę Ziemi.

- Haversine - Dokładna odległość na kuli ziemskiej, uwzględnia jej krzywiznę.

- Manhattan - Ruch po siatce ulic (tylko góra/dół, lewo/prawo), jak w miastach.

```python
def euclidean_distance(node1, node2):
    return sqrt((node1.lat - node2.lat) ** 2 + (node1.lon - node2.lon) ** 2) * 111000 #deg to m

def haversine_distance(node1, node2):
    R = 6371  #earth radius (km)
    lat1, lon1 = radians(node1.lat), radians(node1.lon)
    lat2, lon2 = radians(node2.lat), radians(node2.lon)
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c * 1000  #meters


def manhattan_distance(node1, node2):
    return (abs(node1.lat - node2.lat) + abs(node1.lon - node2.lon)) * 111000 #deg to m
```

# Zadanie 2. Tabu search

### Opis teoretyczny metody
Tabu search to metaheurystyka optymalizacyjna, która iteracyjnie przeszukuje przestrzeń rozwiązań poprzez lokalne modyfikacje aktualnego rozwiązania. Wykorzystuje listę tabu, aby unikać powtarzania tych samych stanów i zapobiegać utknięciu w minimach lokalnych. Głównym celem jest znalezienie optymalnej permutacji punktów przystankowych, minimalizując koszt podróży.

### Przykładowe zastosowania
optymalizacja tras przejazdu pojazdów transportu publicznego, minimalizacja kosztów logistycznych w planowaniu dostaw, usprawnienie harmonogramowania tras

### Wprowadzone modyfikacje
- zastosowanie wcześniej zaimplementowanego algorytmu A* z heurystyką Manhattan
- Ograniczono rozmiar listy tabu do max(7, len(stop_list)), aby uniknąć nadmiernego wzrostu pamięciowego.
- Wprowadzono maksymalną liczbę iteracji (max_iterations = 100), aby zapewnić zakończenie działania algorytmu.
- Wprowadzono listę tabu w modelu FIFO, aby stopniowo usuwać najstarsze zakazane rozwiązania.


### generate_neighbourhood()

Generuje sąsiedztwo rozwiązania.

### calculate_cost()

Dla każdej pary przystanków w rozwiązaniu liczy koszty (wykorzystując algorytm A*), a następnie je sumuje.

Zadanie było bardzo czasochłonne, ale też i niezwykle ciekawe. Podczas implementacji zostało przetestowane wiele różnych modyfikacji oraz heurystyk. Nie wszystkie działają idealnie, ale niektóre wielce usprawniły działanie algorytmów, nawet o kilka sekund. Ustalenie trasy nie było najtrudniejszym zadaniem. Największym wyzwaniem było wyznaczenie jej tak, aby była optymalna pod kątem przesiadek. 
