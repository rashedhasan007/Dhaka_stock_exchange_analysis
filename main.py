import requests
from bs4 import BeautifulSoup

URL = "https://www.amarstock.com/dse-stock-news?symbol=SINGERBD"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")
u=soup.find_all('div', class_='small-12 medium-10 large-10 columns')
print(u)