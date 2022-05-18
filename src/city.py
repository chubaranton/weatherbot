from typing import Dict, List, Any

from bs4 import BeautifulSoup
import requests
import src.magicconstants as mc

def parse(city: str):
    """Запрос в gson-data"""
    URL = mc.site + city.lower()
    HEADERS=mc.HEADERS

    response = requests.get(URL, headers=HEADERS)
    soup = BeautifulSoup(response.content, 'html.parser')
    items = soup.findAll('div', class_='tabsContentInner')
    weather: List[Dict[str, Any]] = []

    for item in items:
        weather.append({
            'temp': item.find('p', class_='today-temp').get_text(strip=True),
            'description': item.findAll('div', class_='description'),
            'feels like': item.findAll('td', class_='cur')[3].get_text(strip=True),
            'pressure': item.findAll('td', class_='cur')[4].get_text(strip=True),
            'humidity': item.findAll('td', class_='cur')[5].get_text(strip=True),
            'wind': item.findAll('td', class_='cur')[6].get_text(strip=True),
        })

    try:
        if(len(weather[0]['description']) == 3):
            weather[0]['description'] = weather[0]['description'][1].get_text(strip=True) + '\n'\
                                        + weather[0]['description'][0].get_text(strip=True).capitalize() + '.'
        else:
            weather[0]['description'] = weather[0]['description'][0].get_text(strip=True)
    except IndexError:
        return None
    return weather