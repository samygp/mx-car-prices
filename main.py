import requests
from bs4 import BeautifulSoup
import json

offset = 0
URL = 'https://www.autocosmos.com.mx/clasificados/busqueda/usados/?sort=2'
page = requests.get(URL)

soup = BeautifulSoup(page.content, 'html.parser')

articles = soup.find_all('article', class_='listing-card')

for a in articles:
    brand = a.find('span', class_='listing-card__brand')
    model = a.find('span', class_='listing-card__model')
    version = a.find('span', class_='listing-card__version')
    year = a.find('span', class_='listing-card__year')
    km = a.find('span', class_='listing-card__km')
    price = a.find('span', class_='listing-card__price-value')
    result = (brand, model, version, year, km, price)
    if None in result:
        continue
    #price = price['content']
    #km = km.replace(' km', '')
    print([x.text for x in result])