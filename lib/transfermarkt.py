# utility functions for accessing transfermarkt.com

from urllib2 import urlopen, Request
from bs4 import BeautifulSoup
from pandas import DataFrame

# transfermarkt blocks default useragent
useragent = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'
# "lol" can be anything - transfermarkt ignores it/uses it for semantic url
urlprefix = 'http://www.transfermarkt.com/lol/'

def getUrlForLeagueId(id, season=2015):
    return urlprefix + 'startseite/wettbewerb/' + id + '/saison_id/' + str(season)

def getUrlForClubId(id, season=2015):
    return urlprefix + 'startseite/verein/' + str(id) + '/saison_id/' + str(season)

def getUrlForPlayerId(id):
    return urlprefix + 'profil/spieler/' + str(id)

def getClubsForLeagueId(id, season=2015):
    bs = BeautifulSoup(urlopen(Request(getUrlForLeagueId(id, season), headers={'User-Agent': useragent})))
    elements = bs.find(id='yw1').find_all("td",class_="hauptlink no-border-links hide-for-small hide-for-pad")
    return [{'clubId': e.find("a")["id"], 'name': e.getText()} for e in elements]

def getPlayersForClubId(id, season=2015):
    bs = BeautifulSoup(urlopen(Request(getUrlForClubId(id, season), headers={'User-Agent': useragent})))
    elements = bs.find(id='yw1').find_all("span",class_="hide-for-small")
    return [{'playerId': e.find("a", class_="spielprofil_tooltip")["id"], 
             'name': e.getText()} for e in elements if e.find("a", class_="spielprofil_tooltip")]

def getTransfersForPlayerId(id):
    bs = BeautifulSoup(urlopen(Request(getUrlForPlayerId(id), headers={'User-Agent': useragent})))
    elements = bs.find(class_="transferhistorie").find_all("tr",class_="zeile-transfer")
    dicts = [{'seasonDate': "  ".join([td.getText() for td in e.findAll("td")[:2]]),
      'mv': e.find("td",class_="zelle-mw").getText(),
      'fee': e.find("td",class_="zelle-abloese").getText(),
      'teams': dict(zip(['from','to'],([{'teamId': team.find("a")["id"], 'name': team.getText()}
                                    for team in e.find_all("td", class_="hauptlink no-border-links hide-for-small vereinsname")])))} for e in elements]
    return [{'season': d['seasonDate'].split("  ")[0],
       'date': d['seasonDate'].split("  ")[1],
       'mv': d['mv'], 'fee': d['fee'],
       'fromTeamId': d['teams']['from']['teamId'],
       'fromTeamName': d['teams']['from']['name'].lstrip(),
       'toTeamId': d['teams']['to']['teamId'],
       'toTeamName': d['teams']['to']['name'].lstrip()} for d in dicts]


