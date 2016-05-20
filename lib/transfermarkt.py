# utility functions for accessing transfermarkt.com

from urllib2 import urlopen, Request
from bs4 import BeautifulSoup
from pandas import DataFrame
import pandas as pd
import re
import os.path 
import datetime 

# transfermarkt blocks default useragent
useragent = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'
# "lol" can be anything - transfermarkt ignores it/uses it for semantic url
urlprefix = 'http://www.transfermarkt.com/lol/'

def getUrlByLeagueId(id, season=2015):
    return urlprefix + 'startseite/wettbewerb/' + id + '/saison_id/' + str(season)

def getUrlByClubId(id, season=2015):
    return urlprefix + 'startseite/verein/' + str(id) + '/saison_id/' + str(season)

def getUrlByPlayerId(id):
    return urlprefix + 'profil/spieler/' + str(id)

def getUrlByAgentId(id):
    return urlprefix + 'beraterfirma/berater/' + str(id)

def getClubsByLeagueId(id, season=2015):
    bs = BeautifulSoup(urlopen(Request(getUrlByLeagueId(id, season), headers={'User-Agent': useragent})))
    elements = bs.find(id='yw1').find_all("td",class_="hauptlink no-border-links hide-for-small hide-for-pad")
    return [{'clubId': e.find("a")["id"], 'name': e.getText().strip(u'\xa0 ')} for e in elements]

def getPlayersByClubId(id, season=2015):
    bs = BeautifulSoup(urlopen(Request(getUrlByClubId(id, season), headers={'User-Agent': useragent})))
    elements = bs.find(id='yw1').find_all("span",class_="hide-for-small")
    return [{'playerId': e.find("a", class_="spielprofil_tooltip")["id"], 
             'name': e.getText()} for e in elements if e.find("a", class_="spielprofil_tooltip")]

def getTransfersByPlayerId(id):
    bs = BeautifulSoup(urlopen(Request(getUrlByPlayerId(id), headers={'User-Agent': useragent})))
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

def getPlayerData(id):
    bs = BeautifulSoup(urlopen(Request(getUrlByPlayerId(id), headers={'User-Agent': useragent})))
    elements = bs.find(class_="spielerdaten").find_all("tr") 
    result1 = [{'key': e.find("th").getText().strip().rstrip(':'),'value': e.find("td").getText().strip(), 
            'country': (e.find('img',class_="flaggenrahmen").get("title")) if e.find('img',class_="flaggenrahmen") else "",
            'hrefs' : [a.get("href") for a in e.findAll("a")]} for e in elements]

    result2 = [{'key':e['key'], 'value': (e['value'] 
           + (" COUNTRY:" + e['country'] if e['key'] == 'Place of birth' else '')
           + (" HREFs: " + " ".join(e['hrefs']) if len(e['hrefs']) > 0 else '')).strip()
          } for e in result1]

    result3 = dict([(e['key'],e['value']) for e in result2])
    
    result3["Display name"] = bs.find("h1").getText()
    print "now processing " + result3["Display name"].encode('utf-8')
    result3["Date of birth"] = result3["Date of birth"].split("HREFs:")[0].strip()
    result3["Current club id"] = result3["Current club"].split("/verein/")[-1]
    result3["Current club"] = result3["Current club"].split("HREFs:")[0].strip()
    if "Outfitter" in result3:
        result3["Outfitter"] = result3["Outfitter"].split("HREFs:")[0].strip()
    if "Shoe model" in result3:
        result3["Shoe model"] = result3["Shoe model"].split("HREFs:")[0].strip()
    if "Glove" in result3:
        result3["Glove"] = result3["Glove"].split("HREFs:")[0].strip()
    if "Player's agent" in result3:
        result3["Player's agent id"] = result3["Player's agent"].split("/")[-1].strip()
        result3["Player's agent"] = result3["Player's agent"].split("HREFs:")[0].strip()
    if "Place of birth" in result3:
        result3["Country of birth"] = result3["Place of birth"].split("COUNTRY:")[-1].strip()
        result3["Place of birth"] = result3["Place of birth"].split("COUNTRY:")[0].strip()
    result3["Nationality"] = re.sub('\s+', ' ', result3["Nationality"])
    if "on loan from" in result3:
        result3["on loan from club id"] = result3["on loan from"].split("/verein/")[-1].strip()
        result3["on loan from"] = result3["on loan from"].split("HREFs:")[0].strip()
    if "2nd club" in result3:
        result3["2nd club id"] = result3["2nd club"].split("/verein/")[-1].strip()
        result3["2nd club"] = result3["2nd club"].split("HREFs:")[0].strip()
    if "Social media" in result3:    
        socialmedia = dict([(url.split("//")[-1].split("/")[0].split(".")[-2], url) for url in result3["Social media"].split(" ") if url.startswith("http")])    
        for platform in ['twitter', 'facebook', 'instagram']:
            if platform in socialmedia:
                result3[platform]=socialmedia[platform]
        if len([x for x in socialmedia if not x in ['twitter', 'facebook', 'instagram']]) > 0:
            result3['website']=socialmedia[[x for x in socialmedia if not x in ['twitter', 'facebook', 'instagram']][0]]
        del result3["Social media"]    
    
    return result3
