import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

price_pattern = re.compile(r'\d+\s*€/luna')
rooms_pattern = re.compile(r'\d+\s*camere')
area_pattern = re.compile(r'\d+\s*m²')


def scrape_storia(city, min_price, max_price, num_rooms):
    all_listings = []
    page = 1

    while True:
        url = f'https://www.storia.ro/ro/rezultate/inchiriere/apartament,{num_rooms}-camere/{city}?limit=24&priceMin={min_price}&priceMax={max_price}&by=DEFAULT&direction=DESC&viewType=listing&page={page}'
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            listings = []

            for item in soup.find_all('li', class_='css-o9b79t e1dfeild0'):
                title_element = item.find('span', {'data-cy': 'listing-item-title'})
                if title_element:
                    title = title_element.text.strip()
                else:
                    title = "N/A"

                price = None
                rooms = "N/A"
                area = None
                link = "N/A"

                for span_element in item.find_all('span', class_='css-1cyxwvy ei6hyam2'):
                    text = span_element.text.strip()

                    if re.search(price_pattern, text):
                        price_match = re.search(r'\d+', text)
                        price = int(price_match.group()) if price_match else None
                    elif re.search(rooms_pattern, text):
                        rooms_match = re.search(r'\d+', text)
                        rooms = int(rooms_match.group()) if rooms_match else None
                    elif re.search(area_pattern, text):
                        area_match = re.search(r'\d+', text)
                        area = int(area_match.group()) if area_match else None

                link_element = item.find('a', {'data-cy': 'listing-item-link'})
                if link_element:
                    link = "https://www.storia.ro" + link_element.get('href')

                # Check if price or area is None, and handle the default values accordingly
                price_per_area = price / area if price is not None and area is not None and area != 0 else float('inf')

                listings.append({
                    'Title': title,
                    'Price': price,
                    'Rooms': rooms,
                    'Area': area,
                    'Link': link,
                    'PricePerArea': price_per_area
                })

            if not listings:
                break  # Break the loop if there are no more listings on the page

            if listings == all_listings[-len(listings):]:
                break  # Break the loop if the list is the same as the previous one

            all_listings.extend(listings)
            page += 1


    # Sort the listings based on price per area
    sorted_listings = sorted(all_listings, key=lambda x: x['PricePerArea'])
    print(page)

    return sorted_listings[:-page+1]


def main():
    check = input("Bucuresti? (y/n): ")
    if check == "y":
        sector = input('Ce sector? (doar cifra -> ex. Sectorul 2 -> 2): ')
        if sector not in ['1', '2', '3', '4', '5', '6', ]:
            print("Nu ati dat un sector valid!")
            return 0
        checkzona = input('Ce zona? (daca nu doresti sa specifici zona scrie n, altfel scrie zona): ')
        if checkzona == "n":
            city = 'bucuresti/' + 'sectorul-' + sector.lower()
        else:
            city = 'bucuresti/' + 'sectorul-' + sector.lower() + '/' + checkzona.lower()

    elif check == 'n':
        city = input('Introdu orasul: ')
    else:
        print("Introdu valoarea corecta (y/n)!")
        return 0

    print("Acum cateva filtre: ")
    min_price = input('Care este pretul minim? (pune 0 daca nu conteaza): ')
    if min_price.isdigit()!=True:
        print("Introdu o valoare corecta! (Numerica)")
        return 0
    max_price = input('Care este pretul maxim?: ')
    if max_price.isdigit()!=True:
        print("Introdu o valoare corecta! (Numerica)")
        return 0

    num_rooms = input('Cate camere?: ')
    if num_rooms.isdigit()!=True:
        print("Introdu o valoare corecta! (Numerica)")
        return 0

    print()



    sorted_listings = scrape_storia(city, min_price, max_price, num_rooms)

    df = pd.DataFrame(sorted_listings)
    if check!='y':
        excel_filename=f'scraped_{city}_{min_price}€_{max_price}€_{num_rooms} camere.xlsx'
    elif checkzona == 'n':
        excel_filename = f'scraped_{sector}_{min_price}€_{max_price}€_{num_rooms} camere.xlsx'
    else:
        excel_filename = f'scraped_{checkzona}_{min_price}€_{max_price}€_{num_rooms} camere.xlsx'

    df.to_excel(excel_filename, index=False)

    print(f'Datele au fost exportate în {excel_filename}.')

    for listing in sorted_listings:
        print(f"Title: {listing['Title']}")
        print(f"Price: {listing['Price']} €")
        print(f"Rooms: {listing['Rooms']}")
        print(f"Area: {listing['Area']} m²")
        print(f"Price per Area: {listing['PricePerArea']} €/m²")
        print(f"Link: {listing['Link']}")
        print()

    print('Am printat: ')
    print(len(sorted_listings))

main()
