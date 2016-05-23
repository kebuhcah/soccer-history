from transfermarkt import *

def getSeasonSideFile(season,side,leagues):
    clubs=[]
    file = "data/clubs/"+side+"_"+str(season)+".csv"
    if os.path.isfile(file):
        print str(datetime.datetime.now()), "skipping", side, season
    else:
        for league in leagues:
            print str(datetime.datetime.now()), "processing", league, season
            try:
                result=getClubsByLeagueId(league)
                [club.update({'league': league}) for club in result]
                clubs.extend(result)
            except Exception as e:
                print str(datetime.datetime.now()), "error", e
        DataFrame(clubs).to_csv(file,index=False,encoding='utf-8')
        print str(datetime.datetime.now()), "finished", side, season

for season in range(2015,2000,-1):
    getSeasonSideFile(season,"top",tier1)
    getSeasonSideFile(season,"bottom",tier2+tier3+youthLeagues)
    getSeasonSideFile(season,"other",otherEurope)
    getSeasonSideFile(season,"world",world)
    getSeasonSideFile(season,"americas",americas)
