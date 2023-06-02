from json import loads
import matplotlib.pyplot as plt
import pandas as pd
from requests import get
from terminaltables import AsciiTable

CITIES = ['Gdańsk', 'Warszawa', 'Elbląg', 'Koszalin', 'Katowice', 'Przemyśl']
CSV_FILE = 'pogoda.csv'

def get_data():
    url = 'https://danepubliczne.imgw.pl/api/data/synop'
    response = get(url)
    rows = [
        ['Miasto', 'Data pomiaru', 'Godzina pomiaru', 'Temperatura', 'Ciśnienie']
    ]
    for row in loads(response.text):
        if row['stacja'] in CITIES:
            rows.append([
                row['stacja'],
                row['data_pomiaru'],
                row['godzina_pomiaru'],
                row['temperatura'],
                row['cisnienie']
            ])
    table = AsciiTable(rows)
    print(table.table)

    # Zapisanie danych do pliku CSV
    with open(CSV_FILE, 'w', encoding='utf-8') as f:
        for row in rows:
            f.write(','.join(str(x) for x in row) + '\n')

def plot_data():
    # Wczytanie danych z pliku CSV do ramki danych
    df = pd.read_csv(CSV_FILE)

    # Analiza danych przy użyciu Pandas
    # Przykładowa analiza: podsumowanie statystyk dla temperatury i ciśnienia
    temperature_stats = df['Temperatura'].describe()
    pressure_stats = df['Ciśnienie'].describe()
    print('Statystyki temperatury:')
    print(temperature_stats)
    print('Statystyki ciśnienia:')
    print(pressure_stats)

    # Wizualizacja danych za pomocą Matplotlib
    # Wykres kołowy dla średniej temperatury dla każdego miasta
    avg_temperature = df.groupby('Miasto')['Temperatura'].mean()
    plt.figure(figsize=(8, 8))
    plt.pie(avg_temperature, labels=avg_temperature.index, autopct='%1.1f%%')
    plt.title('Średnia temperatura dla miast')
    plt.axis('equal')
    plt.tight_layout()
    plt.show()

    # Wykres słupkowy dla średniej temperatury
    plt.figure(figsize=(10, 6))
    plt.bar(avg_temperature.index, avg_temperature)
    plt.xlabel('Miasto')
    plt.ylabel('Średnia temperatura [°C]')
    plt.title('Wykres słupkowy średniej temperatury')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    # Wykres punktowy dla zależności temperatury od ciśnienia
    plt.figure(figsize=(10, 6))
    for city in CITIES:
        city_data = df[df['Miasto'] == city]
        plt.scatter(city_data['Ciśnienie'], city_data['Temperatura'], label=city, s=100)
    plt.xlabel('Ciśnienie [hPa]')
    plt.ylabel('Temperatura [°C]')
    plt.title('Wykres punktowy: Temperatura a ciśnienie')
    plt.legend()
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    print('Pogodynka')
    get_data()
    plot_data()
