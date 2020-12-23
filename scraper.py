import requests
from bs4 import BeautifulSoup

class Scraper:

  def __init__(self):
    self.url = 'https://www.goal.com/br/not%C3%ADcias/programacao-partidas-futebol-tv-aberta-fechada-onde-assistir/1jf3cuk3yh5uz18j0s89y5od6w'
    self.response = requests.get(self.url)
    self.soup = BeautifulSoup(self.response.text, 'html.parser')
    self.returns = self.soup.find('table', attrs={'class': 'tableizer-table'})
    self.tds = self.returns.find_all('td')
    self.all_games = self.html_to_dict()

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

  def html_to_dict(self):
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

  def get_all_games(self):
    return self.all_games

  def change_channel(self):
    new = self.all_games
    for game in new:
      changed = False
      if 'SporTV' in game['channel']:
        game['channel'] = game['channel'].replace('SporTV', 'SportTV (canal 539 ou 538 ou 537)')
      if 'Premiere' in game['channel']:
        game['channel'] = game['channel'].replace('Premiere', 'Premiere (canal 721 ou 722 ou 723 ou 724 ou 725 ou 726 ou 727)')
      if 'EI Plus' in game['channel']:
        game['channel'] = game['channel'].replace('EI Plus', 'EIPlus (internet)')
      if 'ESPN Brasil' in game['channel']:
        game['channel'] = game['channel'].replace('ESPN Brasil', 'ESPN Brasil (canal 570)')
        changed = True
      if 'ESPN App' in game['channel']:
        game['channel'] = game['channel'].replace('ESPN App', 'ESPN App (internet)')
        changed = True
      if 'Fox Sports' in game['channel']:
        game['channel'] = game['channel'].replace('Fox Sports', 'Fox Sports (canal 573)')
      if 'ESPN' in game['channel'] and changed == False:
        game['channel'] = game['channel'].replace('ESPN', 'ESPN (canal 571)')
      if 'Band Sports' in game['channel']:
        game['channel'] = game['channel'].replace('Band Sports', 'Band Sports (canal 575)')
      
    return new
        
  def get_br_games(self):
    br_games = []
    for game in self.all_games:
      if(game['championship'] == 'Série B' or game['championship'] == 'Copa do Brasil' or game['championship'] == 'Libertadores'):
        br_games.append(game)

    return br_games
 
  def get_total_games(self):
    return len(self.all_games)

test = Scraper()
# print(test.get_all_games()) 
# print(test.get_br_games()) 
a = test.change_channel()
total_games = test.get_total_games()
for element in a:
  print(element)

print(total_games, ' jogos hoje!')
