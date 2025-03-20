import sys
import csv
import time
from datetime import datetime



#algorytm wyszukiwania najkrótszych połączeń pomiędzy zadanymi przystankami A i B
#miarę odległości, zależnie od decyzji użytkownika, czas dojazdu z A do B lub liczba przesiadek koniecznych do wykonania

#input:
#przystanek start A
#przystanek end B
#kryt. opt.: wartość t oznacza minimalizację czasu dojazdu, wartość p oznacza minimalizację liczby zmian linii
#czas pojawienia się na przystanku początkowym


def format_time(timestamp):
    return timestamp.strftime("%Y-%m-%d %H:%M:%S.%f")[:-4]

#format: ['4136', 'MPK Autobusy', 'A', '05:18:00', '05:19:00', 'FAT', 'GRABISZYŃSKA (Cmentarz)', '51.09412632', '16.9783528', '51.08990377', '16.97664203']
#print first 10 lines for debug
with open('connection_graph.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    
    # Otwórz plik do zapisu
    with open('output.csv', mode='w', newline='', encoding='utf-8') as outputfile:
        writer = csv.writer(outputfile)
        
        # Iteracja przez wiersze i zapisanie tych, które spełniają warunek
        for line in reader:
            if line[2] == '149' and line[5] == 'most Grunwaldzki':
                writer.writerow(line)
                
                
start_time = datetime.now()
print(f"Start time: {format_time(start_time)}")
        
sys.stdout.write("To jest stdout\n")
sys.stdout.write("To jest stderr\n")
time.sleep(1)
end_time = datetime.now()
print(f"End time: {format_time(end_time)}")
#stdout:
#harmonogram przejazdu, wypisując w kolejnych liniach informacje o kolejno wykorzystanych liniach komunikacyjnych (nazwa linii, czas i przystanek, na którym wsiadamy do danej linii komunikacyjnej oraz czas i przystanek,
#na którym kończymy korzystać z danej linii). 

#stderr:
#wartość funkcji kosztu znalezionego rozwiązania oraz czas obliczeń liczony od wczytania danych do uzyskania rozwiązania.