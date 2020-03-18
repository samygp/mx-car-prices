import requests
from bs4 import BeautifulSoup
import json
import pandas as pd

def parse_article(a):
    try:
        result = {
            "url": a.find('a', attrs={"itemprop": "url"})['href'],
            "brand": a.find('span', class_='listing-card__brand').text,
            "model": a.find('span', class_='listing-card__model').text,
            "version": a.find('span', class_='listing-card__version').text,
            "year": a.find('span', class_='listing-card__year').text,
            "km": a.find('span', class_='listing-card__km').text,
            "price": a.find('span', class_='listing-card__price-value')['content']
        }
        if None in result.values():
            return None
        return result
    except Exception as e:
        print("Error parsing article:", e)
    return None

def get_listing(y_start, y_end, listing):
    done = False
    page_index = 1
    print(f"Buscar de {y_start} hasta {y_end}")
    while not done:
        try:
            URL = f'https://www.autocosmos.com.mx/clasificados/busqueda/usados/?aa={y_start}-{y_end}&pageindex={page_index}&sort=2'
            print("\nQuerying", URL)
            page = requests.get(URL)
            soup = BeautifulSoup(page.content, 'html.parser')
            articles = soup.find_all('article', class_='listing-card')
            for a in articles:
                car = parse_article(a)
                if car is not None:
                    listing.append(car)
            nxt = soup.find_all('a', class_='m-next')
            done = len(nxt) == 0
            page_index += 1
        except Exception as e:
            print("Something went wrong:", e)
            done = True
    return listing

y_start = 2000
y_end = 2001
listing = []
for i in range(0,19,2):
    get_listing(y_start + i, y_end + i, listing)

df = pd.DataFrame(listing)
print(df.head())
df.to_csv('../data/carros_raw.csv')