from transfermarkt import *

for league in ['GB1','ES1','L1','FR1','IT1','PO1','NL1','MLS1','TR1','RU1','GB2','BE1']:
    for season in range(2001,2016)[::-1]:

        filename=league+'_'+str(season)
        personalFile='data/personal/'+filename+'.csv'
        transfersFile='data/transfers/'+filename+'.csv'
        indexFile='data/index/'+filename+'.csv'
        if os.path.isfile(personalFile) and os.path.isfile(transfersFile) \
            and (not 'error' in pd.read_csv(personalFile).columns) \
            and (not 'error' in pd.read_csv(transfersFile).columns):
            print str(datetime.datetime.now()), filename, "files already complete"
        elif not os.path.isfile(indexFile):
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
                if not 'id' in oldTransfers.columns:
                    print "bad transfers file"
                elif 'error' in oldTransfers.columns:
                    transfersTodo = [id for id in index.index \
                            if not id in oldTransfers[pd.isnull(oldTransfers['error'])]['id'].tolist()]
                else:
                    transfersTodo = [id for id in index.index if not id in oldTransfers['id'].tolist()]
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
                if id in personalTodo:
                    try:
                        data = getPlayerDataFromBs(bs)
                        data.update({'id':id})
                    except Exception as e:
                        print "personal error", e
                        data = {'id':id, 'error': e}
                    dataList.append(data)
                if id in transfersTodo:
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
                    transfersOutput = pd.concat([oldTransfers,transfersOutput], ignore_index=True)
                transfersOutput.to_csv(transfersFile,index=False,encoding='utf-8')
            print str(datetime.datetime.now()), "done"