from transfermarkt import *

for league in tier1 + otherEurope:
    file = "data/tables/"+league+".csv"
    if os.path.isfile(file):
        print str(datetime.datetime.now()), "skipping", league
    else:
        print str(datetime.datetime.now()), "processing", league
        try:
            result=pd.concat([getTableByLeagueId(league,season) for season in range(2015,1989,-1)])
            result.to_csv(file,index=False,encoding='utf-8')
            print str(datetime.datetime.now()), "finished", league
        except Exception as e:
            print str(datetime.datetime.now()), "error", e
