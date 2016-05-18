# utility functions for accessing transfermarkt.com

from urllib2 import urlopen, Request
from bs4 import BeautifulSoup
from pandas import DataFrame

useragent = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'
urlprefix = 'http://www.transfermarkt.com/lol/'

def getUrlFromLeagueId(id, season=2015):
    return urlprefix + 'startseite/wettbewerb/' + id + '/saison_id/' + str(season)

def getClubsFromLeagueId(id, season=2015):
    bs = BeautifulSoup(urlopen(Request(getUrlFromLeagueId(id, season), headers={'User-Agent': useragent})))
    elements = bs.find(id='yw1').find_all("td",class_="hauptlink no-border-links hide-for-small hide-for-pad")
    return DataFrame([{'id': cp.find("a")["id"], 'name': cp.getText(), 'url': cp.find("a")["href"]} for cp in elements])

def getUrlFromClubId(id, season=2015):
    return urlprefix + 'startseite/verein/' + str(id) + '/saison_id/' + str(season)

def getPlayersFromClubId(id, season=2015):
    bs = BeautifulSoup(urlopen(Request(getUrlFromClubId(418), headers={'User-Agent': useragent})))
    elements = bs.find(id='yw1').find_all("span",class_="hide-for-small")
    return DataFrame([{'id': cp.find("a", class_="spielprofil_tooltip")["id"], 'name': cp.getText(), 'url': cp.find("a")["href"]} for cp in elements 
                      if cp.find("a", class_="spielprofil_tooltip")])

def getUrlFromPlayerId(id):
    return urlprefix + 'profil/spieler/' + str(id)
