from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import pandas as pd
from bs4 import BeautifulSoup
import re
from datetime import datetime

s = Service('/Users/maliabarker/Desktop/main/MakeSchool/Term4/ACS_2511/chromedriver')
driver = webdriver.Chrome(service=s)

'''
* Previous website attempts *
https://cookieandkate.com/recipes/
https://pinchofyum.com/recipes/all
'''
urls = ['http://www.seasky.org/astronomy/astronomy-calendar-2020.html', 'http://www.seasky.org/astronomy/astronomy-calendar-2021.html', 'http://www.seasky.org/astronomy/astronomy-calendar-2022.html', 'http://www.seasky.org/astronomy/astronomy-calendar-2023.html', 'http://www.seasky.org/astronomy/astronomy-calendar-2024.html', 'http://www.seasky.org/astronomy/astronomy-calendar-2025.html', 'http://www.seasky.org/astronomy/astronomy-calendar-2026.html', 'http://www.seasky.org/astronomy/astronomy-calendar-2027.html', 'http://www.seasky.org/astronomy/astronomy-calendar-2028.html', 'http://www.seasky.org/astronomy/astronomy-calendar-2029.html', 'http://www.seasky.org/astronomy/astronomy-calendar-2030.html']

new_moons = []
full_moons = []
lunar_eclipses = []
solar_eclipses = []
planetary_events = []
equinox_solstice = []
meteor_showers = []
new_df = pd.DataFrame(columns=['eventName', 'description', 'img', 'date', 'dt', 'calendar', 'color', 'cont'])

def create_new_event(cont, img, calendar, color):
    # eventName 
        # contained in span tag with title-text class
    # description
        # After title-text span tag, just floating in p tag
    # img
        # Specific to event, pull from img names from original repo
    # date in UTC format
    # dt (month day, year ex: January 17, 2022) 
        # contained in span tag with class date-text 
        # need to add year
        # need to check if there are two dates, if there are, split into two separate things
    global new_df
    img = img
    eventName = cont.find('span', {'class': 'title-text'}).text
    description = cont.text.split(eventName)[-1].strip()
    eventName = eventName.replace(".", "").replace('"', "")
    if img == None:
        if 'jupiter' in eventName.lower():
            img = "/static/images/jupiter.png"
        elif 'mars' in eventName.lower():
            img = "/static/images/mars.png"
        elif 'mercury' in eventName.lower():
            img = "/static/images/mercury.png"
        elif 'neptune' in eventName.lower():
            img = "/static/images/neptune.png"
        elif 'saturn' in eventName.lower():
            img = "/static/images/saturn.png"
        elif 'uranus' in eventName.lower():
            img = "/static/images/uranus.png"
        elif 'venus' in eventName.lower():
            img = "/static/images/venus.png"
    date = cont.find('span', {'class': 'date-text'}).text.strip()
    if ',' in date:
        date_list = date.split()
        month = date_list[0].strip()
        dates = [int(re.sub('[^0-9]', '', item)) for item in date_list if re.search('[0-9]', item)]
        for day in dates:
            date_str = f'{month} {day}, {year_str}'
            date_obj = datetime.strptime(date_str, "%B %d, %Y")
            iso_date_str = date_obj.isoformat()
            # print({'eventName': eventName, 'description': description, 'img': img, 'date': iso_date_str, 'dt': date_str, 'cont': cont})
            if cont not in new_df['cont'].values:
                new_df = new_df.append({'eventName': eventName, 'description': description, 'img': img, 'date': iso_date_str, 'dt': date_str, 'calendar': calendar, 'color': color, 'cont': cont}, ignore_index=True)
    else:
        date_str = date + ", " + year_str  # assuming you have the year stored somewhere
        date_obj = datetime.strptime(date_str, "%B %d, %Y")
        iso_date_str = date_obj.isoformat()
        # print({'eventName': eventName, 'description': description, 'img': img, 'date': iso_date_str, 'dt': date_str, 'cont': cont})
        if cont not in new_df['cont'].values:
            new_df = new_df.append({'eventName': eventName, 'description': description, 'img': img, 'date': iso_date_str, 'dt': date_str, 'calendar': calendar, 'color': color, 'cont': cont}, ignore_index=True)

i = 0

while i <= len(urls) - 1:
    driver.get(urls[i])

    content = driver.page_source
    soup = BeautifulSoup(content, features="html.parser")
    
    # get year
    input_str = str(soup.find('h1'))
    match = re.search(r"\d{4}", input_str)
    year_str = match.group()

    for b1 in soup.findAll(attrs={'class': 'b1'}):
        # for new moons
        cont = b1.find('p')
        create_new_event(cont, "/static/images/newmoon.png", 'Moon Event', 'blue')
        if cont not in new_moons:
            new_moons.append(cont.text)


    for b2 in soup.findAll(attrs={'class': 'b2'}):
        # for full moons
        cont = b2.find('p')
        create_new_event(cont, "/static/images/fullmoon.png", 'Moon Event', 'blue')
        if cont not in full_moons:
            full_moons.append(cont.text)

    for b3 in soup.findAll(attrs={'class': 'b3'}):
        # for lunar eclipses
        cont = b3.find('p')
        create_new_event(cont, "/static/images/lunareclipse.png", 'Moon Event', 'blue')
        if cont not in lunar_eclipses:
            lunar_eclipses.append(cont.text)

    for b4 in soup.findAll(attrs={'class': 'b4'}):
        # for solar eclipses
        cont = b4.find('p')
        create_new_event(cont, "/static/images/solareclipse.png", 'Solar Event', 'yellow')
        if cont not in solar_eclipses:
            solar_eclipses.append(cont.text)

    for b5 in soup.findAll(attrs={'class': 'b5'}):
        # for planetary events
        cont = b5.find('p')
        create_new_event(cont, None, 'Planetary Event', 'orange')
        if cont not in planetary_events:
            planetary_events.append(cont.text)

    for b8 in soup.findAll(attrs={'class': 'b8'}):
        # for equinoxes and solstices
        cont = b8.find('p')
        create_new_event(cont, "/static/images/sun.png", "Solar Event", 'yellow')
        if cont not in equinox_solstice:
            equinox_solstice.append(cont.text)

    for b9 in soup.findAll(attrs={'class': 'b9'}):
        # for meteor showers
        cont = b9.find('p')
        create_new_event(cont, "/static/images/meteor3.png", "Meteors, Comets, & Asteroids", 'green')
        if cont not in meteor_showers:
            meteor_showers.append(cont.text)

    for b11 in soup.findAll(attrs={'class': 'b11'}):
        # for asteroids
        cont = b11.find('p')
        create_new_event(cont, "/static/images/asteroid.png", "Meteors, Comets, & Asteroids", 'green')
    
    i+=1


series0 = pd.Series(new_moons, name = 'NewMoons')
series1 = pd.Series(full_moons, name = 'FullMoons')
series2 = pd.Series(lunar_eclipses, name = 'LunarEclipses')
series3 = pd.Series(solar_eclipses, name = 'SolarEclipses')
series4 = pd.Series(planetary_events, name = 'PlanetaryEvents')
series5 = pd.Series(equinox_solstice, name = 'EquinoxesSolstices')
series6 = pd.Series(meteor_showers, name = 'MeteorShowers')

df = pd.DataFrame({'NewMoons': series0, 'FullMoons': series1, 'LunarEclipses': series2, 'SolarEclipses': series3, 'PlanetaryEvents': series4, 'EquinoxesSolstices': series5, 'MeteorShowers': series6})
df.to_csv('celestial_events.csv', index=False, encoding='utf-8')
new_df.to_csv('celestial_events2.csv', index=False, encoding='utf-8')

if __name__ == '__main__':
    # for testing purposes
    for x in meteor_showers:
        print(x)