import requests
from bs4 import BeautifulSoup
from html2json import collect

class Scraper:

  def __init__(self):
    self.url = 'https://www.goal.com/br/not%C3%ADcias/programacao-partidas-futebol-tv-aberta-fechada-onde-assistir/1jf3cuk3yh5uz18j0s89y5od6w'
    self.response = requests.get(self.url)
    self.soup = BeautifulSoup(self.response.text, 'html.parser')
    self.returns = self.soup.find('table', attrs={'class': 'tableizer-table'})
    self.tds = self.returns.find_all('td')
    self.all_games = self.get_all_games()

  def clear_string(self, string):
    new_string = ''
    tag = False
    for c in string:
      if c == '<':
        tag = True
      elif c == '>':
        tag = False
      
      if tag == False:
        new_string += c

    return new_string

  def get_all_games(self):
    games = []
    aux = 0
    for td in self.tds:
      if(aux == 0):
        example = {}
        example['game'] = self.clear_string(td.text)
      elif(aux == 1):
        example['championship'] = self.clear_string(td.text)
      elif(aux == 2):
        example['hour'] = self.clear_string(td.text)
      elif(aux == 3):
        example['channel'] = self.clear_string(td.text)
      
      aux = aux + 1
      if aux == 5:
        aux = 0
        games.append(example)
    return games

    
        
  def get_br_games(self):
    br_games = []
    for game in self.all_games:
      if(game['championship'] == 'Série B' or game['championship'] == 'Copa do Brasil' or game['championship'] == 'Libertadores'):
        br_games.append(game)

    return br_games
 

test = Scraper()
print(test.get_all_games()) 
# print(test.get_br_games()) 