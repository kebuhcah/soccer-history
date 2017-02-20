from transfermarkt import *
import sys

def extractLeagues(leagues):
    for league in leagues:
        for season in range(2001,2017)[::-1]:
            filename=league+'_'+str(season)
            personalFile='data/personal/'+filename+'.csv'
            transfersFile='data/transfers/'+filename+'.csv'
            indexFile='data/index/'+filename+'.csv'
            if not os.path.isfile(indexFile):
                print str(datetime.datetime.now()), filename, "index file missing!"
            else:
                print str(datetime.datetime.now()), "retrieving", filename
                index = pd.read_csv(indexFile, index_col=0,names=['name'])
                personalTodo = index.index.tolist()
                if os.path.isfile(personalFile):
                    oldPersonal = pd.read_csv(personalFile)
                    if not 'id' in oldPersonal.columns:
                        print "bad personal file"
                    elif 'error' in oldPersonal.columns:
                        personalTodo = [id for id in index.index \
                                if not id in oldPersonal[pd.isnull(oldPersonal['error'])]['id'].tolist()]
                    else:
                        personalTodo = [id for id in index.index if not id in oldPersonal['id'].tolist()]
                transfersTodo = index.index.tolist()
                if os.path.isfile(transfersFile):
                    oldTransfers = pd.read_csv(transfersFile)
                    if (not 'id' in oldTransfers.columns) or (not 'playerName' in oldTransfers.columns):
                        print "bad transfers file"
                    else:
                        transfersTodo = [id for id in index.index if not id in oldTransfers[pd.notnull(oldTransfers['playerName'])]['id'].tolist()]
                dataList=[]
                transfersList=[]
                todo = set(personalTodo+transfersTodo)
                if len(todo) == 0:
                    print str(datetime.datetime.now()), "no missing ids, done"
                    continue
                for id in list(todo):
                    try:
                        bs = getBsByPlayerId(id)
                    except Exception as e:
                        print "url error", e
                        bs = None
                    if bs != None and id in personalTodo:
                        try:
                            data = getPlayerDataFromBs(bs)
                            data.update({'id':id})
                        except Exception as e:
                            print "personal error", e
                            data = {'id':id, 'error': e}
                        dataList.append(data)
                    if bs != None and id in transfersTodo:
                        transfers = [{'id':id, 'error': 'idk'}]
                        try:
                            transfers = getTransfersFromBs(bs)
                            [transfer.update({'id':id}) for transfer in transfers]
                        except Exception as e:
                            print "transfers error", e
                            transfers = [{'id':id, 'error': e}]
                        transfersList.append(transfers)
                personalFrame = DataFrame(dataList,index=[row["id"] for row in dataList])
                personalOutput = index
                if os.path.isfile(personalFile):
                    oldPersonal = pd.read_csv(personalFile)
                    if 'id' in oldPersonal.columns:
                        oldPersonal.index = oldPersonal['id']
                        if 'error' in oldPersonal.columns:
                            oldPersonal = oldPersonal.drop('error',axis=1)
                        personalOutput = personalOutput.merge(oldPersonal,how='left',left_index=True,right_index=True,suffixes=['_XX',''])
                        personalOutput = personalOutput[[c for c in personalOutput.columns if not c.endswith('_XX')]]
                personalOutput = personalOutput.merge(personalFrame,how='left',left_index=True,right_index=True,suffixes=['_XX',''])
                for cxx in personalOutput.columns:
                    if cxx.endswith('_XX'):
                        c = cxx[:-3]
                        personalOutput[c]=np.where(pd.isnull(personalOutput[c]),personalOutput[cxx],personalOutput[c])
                personalOutput = personalOutput[[c for c in personalOutput.columns if not c.endswith('_XX')]]
                personalOutput.to_csv(personalFile,index=False,encoding='utf-8')
                if len(transfersList) > 0:
                    transfersOutput = pd.concat([DataFrame(transfers) for transfers in transfersList], ignore_index=True)
                    if os.path.isfile(transfersFile):
                        oldTransfers = pd.read_csv(transfersFile)
                        if 'error' in oldTransfers.columns:
                            oldTransfers = oldTransfers.drop('error',axis=1)
                        transfersOutput = pd.concat([oldTransfers,transfersOutput], ignore_index=True)
                    transfersOutput.drop_duplicates().to_csv(transfersFile,index=False,encoding='utf-8')
                print str(datetime.datetime.now()), "done"

#['GB1','ES1','L1','FR1','IT1','PO1','NL1','MLS1','TR1','RU1','GB2','BE1']

#python lib/playerdata.py GB1 IT1 TR1
#python lib/playerdata.py ES1 PO1 RU1
#python lib/playerdata.py L1 NL1 GB2
#python lib/playerdata.py FR1 MLS1 BE1

#python lib/playerdata.py GB1 FR1 NL1 RU1
#python lib/playerdata.py ES1 IT1 MLS1 GB2
#python lib/playerdata.py L1 PO1 TR1 BE1

#python lib/playerdata.py TS1 SLO1
#python lib/playerdata.py SL1 FI1
#python lib/playerdata.py LUX1 AZ1

#'TS1','SLO1','SL1','FI1','LUX1','AZ1'
extractLeagues(sys.argv[1:])
