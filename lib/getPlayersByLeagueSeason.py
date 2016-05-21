from transfermarkt import *
import os
import datetime

for season in range(2001,2016)[::-1]:
    for league in ['GB1','ES1','IT1','L1','FR1','TR1','RU1','PO1','NL1','BE1','GB2','MLS1']:
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
