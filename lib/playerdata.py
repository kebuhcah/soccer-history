from transfermarkt import *

for season in range(2001,2016)[::-1]:
    for league in ['GB1','ES1','IT1','L1','FR1','TR1','RU1','PO1','NL1','BE1','GB2','MLS1']:

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
            dataList=[]
            transfersList=[]
            for id in index.index:
                try:
                    bs = getBsByPlayerId(id)
                except Exception as e:
                    print "error", e
                try:
                    data = getPlayerDataFromBs(bs)
                    data.update({'id':id})
                except Exception as e:
                    print "error", e
                    data = {'id':id, 'error': e}
                dataList.append(data)
                try:
                    transfers = getTransfersFromBs(bs)
                    [transfer.update({'id':id}) for transfer in transfers]
                except Exception as e:
                    transfers = [{'id':id, 'error': e}]
                transfersList.append(transfers)
        DataFrame(dataList).to_csv(personalFile,index=False,encoding='utf-8')
        pd.concat([DataFrame(transfers) for transfers in transfersList], ignore_index=True).to_csv(transfersFile,index=False,encoding='utf-8')
        print str(datetime.datetime.now()), "done"
