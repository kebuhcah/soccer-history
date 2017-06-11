from transfermarkt import *

for season in range(2001,2017)[::-1]:
    for league in tier1+tier2+tier3+youthLeagues+otherEurope+world+americas+defunct+deep:
        filename = "data/rawindex/" + league + "_" + str(season) + ".xls"
        if os.path.isfile(filename):
            print str(datetime.datetime.now()), filename, "already exists"
        else:
            try:
                print str(datetime.datetime.now()), "retrieving", filename
                DataFrame([player for club in getClubsByLeagueId(league,season) \
                            for player in getPlayersByClubId(club['clubId'],season)]).to_excel(filename)
                print str(datetime.datetime.now()), "done"
            except Exception as e:
                print str(datetime.datetime.now()), "error", e
