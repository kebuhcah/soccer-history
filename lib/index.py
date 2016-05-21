from transfermarkt import *

def getPlayersByLeagueSeasonFile(league,season):
    filename = league + "_" + str(season)
    df = pd.read_excel("data/rawindex/" + filename + ".xls",index_col=2,names=['','name'])
    df["filename"]=filename
    return df

players = pd.concat([getPlayersByLeagueSeasonFile(league,season) \
     for season in range(2001,2016) \
     for league in ['GB1','ES1','IT1','L1','FR1','TR1','RU1','PO1','NL1','BE1','GB2','MLS1']])[["name","filename"]] \
    .drop_duplicates(subset='name').sort_index()

[DataFrame(players[players["filename"]==x])["name"].to_csv("data/index/"+x+".csv", encoding='utf-8', index_label='id') \
    for x in players["filename"].drop_duplicates()]
