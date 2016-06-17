from transfermarkt import *

def getPlayersByLeagueSeasonFile(league,season):
    filename = league + "_" + str(season)
    df = pd.read_excel("data/rawindex/" + filename + ".xls",index_col=2,names=['','name'])
    df["filename"]=filename
    df["league"]=league
    df["season"]=season
    return df

players = pd.concat([getPlayersByLeagueSeasonFile(league,season) \
     for season in range(2001,2016) \
     for league in ['GB1','ES1','IT1','L1','FR1','TR1','RU1','PO1','NL1','BE1','GB2','MLS1',
                    'UKR1','GR1','RO1','ZYP1','C1','KR1','SER1','ISR1','SC1','BU1','LI1','MAL1',
                    'PL1','DK1','SE1','NO1','A1','BOS1','KAS1','UNG1','TS1','SLO1','SL1','FI1','LUX1','AZ1','IR1']])[["name","filename","league"]] \
    .drop_duplicates(subset=['name','league']).sort_index()

[DataFrame(players[players["filename"]==x])["name"].to_csv("data/index/"+x+".csv",
    encoding='utf-8', index_label='id') for x in players["filename"].drop_duplicates()]
