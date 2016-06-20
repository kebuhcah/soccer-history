// run this
//count "SSDISSFSSSFSFSSSSSSSSSSSSSSSS"
transfers:("SSZISSFSSSFSFSSSZSSFFSSSSSSSFFFSISFZZSFZSFSSZSSSFZSSSSFSFFS";enlist",")0:`:data/merged/transfers.csv;
update `date$date,`date$dateOfBirth,`date$inTheTeamSince,`date$contractUntil,`date$contractThereUntil,`date$dateOfLastContractExtension,`date$dayOfDeath from `transfers;
update {"D"$(string 100+`year$x),"/",(string`mm$x),"/",(string`dd$x)}each date from `transfers where date<1930.01.01;
update mvDelta:(0n,0^1_deltas mv) by id from `transfers;
update duration:(0Ni,1_deltas date) by id from `transfers;
update {`$"\"",x,"\""}each string placeOfBirth from `transfers;
update {`$"\"",x,"\""}each string period from `transfers;
update {`$"\"",x,"\""}each string countryOfBirth  from `transfers;
update {`$"\"",x,"\""}each string Nationality  from `transfers;
update {`$"\"",x,"\""}each string nationality2  from `transfers;
update {`$"\"",x,"\""}each string currentClub  from `transfers;
update {`$"\"",x,"\""}each string fromLeague  from `transfers;
update {`$"\"",x,"\""}each string fromCountry  from `transfers;
update {`$"\"",x,"\""}each string toLeague  from `transfers;
update {`$"\"",x,"\""}each string toCountry  from `transfers;
update {`$"\"",x,"\""}each string playersAgent  from `transfers;
update {`$"\"",x,"\""}each string nameInHomeCountry  from `transfers;
update {`$"\"",x,"\""}each string fee  from `transfers;
update {`$"\"",x,"\""}each string fromTeamName  from `transfers;
transfers_q:transfers;
nonloans:select from transfers where `False=isLoan;
loans:select from transfers where `True=isLoan;
save`:data/merged/transfers_q.csv  ;
save`:data/merged/nonloans.csv  ;
save`:data/merged/loans.csv  


//end
count","vs(read0`:data/merged/transfers_q.csv)[1907]
count","vs(read0`:data/merged/transfers.csv)[1907]
meta transfers
([]`$(0_(read0`:data/merged/transfers_q.csv)[269132];0_(read0`:data/merged/transfers.csv)[269132]))
first 1_ "\""vs(read0`:data/merged/transfers.csv)[269132]
count cols transfers_q
1000#transfers_q
select from transfers where date<1980.01.01
select from transfers_q where i=49

{"D"$(string 100+`year$x),"/",(string`mm$x),"/",(string`dd$x)}1903.01.01

type 0Ni
meta transfers

`duration`date xcols select from (update i from transfers) where id=`37262
{select key asc duration!period,min duration,sum c by Nationality from x where c>500}select avg duration,c:count i by Nationality,period from select avg duration,count i,first Nationality  by id,period from transfers where season within 2000 2015
683-127+127

select from transfers where null Nationality 

avg 1 2 3 0n

select id,mv,mvDelta,date from transfers where id in exec id from transfers where feeValue>0,mv>0

select count i by fromCountry,toCountry from transfers where mvDelta<0,fromCountry<>toCountry,not null fromCountry,not null toCountry



csv 0: ([]a: 1 2 3;b: `$("";"";"asd,asd"))

select count i by contractOption from transfers

se

// number of countires in career by nationality
{select from x where c>100}select avg countryCount,c:count i by Nationality from update countryCount:count each distinct each countryChain,`$"->"sv/: string countryChain from select first playerName,max feeValue,first Nationality,countryChain:{x where x<>next x}{x where not null x}(fromCountry[0],toCountry) by id from transfers

select from transfers where contractOption=`$"31.0"
deltas 1 2
{select from x where 0<contractlength}select id,inTheTeamSince,contractUntil,contractlength:12*(contractUntil-inTheTeamSince)%366 from select by id from transfers

select

`c xdesc select c:count i by fromCountry,toCountry from transfers where mvDelta<0,isLoan<>`True,fromCountry=`England

balance:`mvDelta xdesc{select from x}{select fromCountry,toCountry,feeValue+negFeeValue,Count+negCount,mvDelta+negMv from(select fromCountry:toCountry,toCountry:fromCountry,negFeeValue:neg feeValue,negCount:neg Count,negMv:neg mvDelta from x)lj x}select sum feeValue,Count:count i,sum mvDelta by fromCountry,toCountry from transfers where fromCountry<>toCountry,season<2010


select from balance where toCountry=`Germany
select fromCountry from balance where toCountry=`England,0.66>prev(sums feeValue)%sum feeValue

getChildren:{{((`$"level",/:(string til -1+count cols x)),`leaf)xcol x} ungroup update newleaf:{{$[0=count x;enlist`;x]}(exec fromCountry from balance where toCountry=x,fromCountry in (exec fromCountry from (select first toCountry by fromCountry from balance) where toCountry=x),1>=prev(sums feeValue)%sum feeValue)}each leaf from x}
 getChildren getChildren getChildren getChildren getChildren([] leaf:enlist`England)

select from balance where toCountry=`England
exec fromCountry from (select first toCountry by fromCountry from balance) where toCountry=`England
,0.66>prev(sums feeValue)%sum feeValue

{(`$"level",/:(string til -1+count cols x),`leaf)xcol x}t
t
{(`$"level",/:(til -1+count cols x),`leaf)xcol x}t


{select from x where id=`52848}
select id,playerName,date,toTeamName,fromTeamName,nextFrom:next fromTeamName,toTeamId,next fromTeamId from transfers where toTeamId<>next fromTeamId, id=next id,isLoan<>`True

","sv"`date$",/:string exec c from (meta transfers)where t="z"

update `date$date,`date$dateOfBirth,`date$inTheTeamSince,`date$contractUntil,`date$contractThereUntil,`date$dateOfLastContractExtension,`date$dayOfDeath from transfers
select count i by contractThereUntil from transfers

update toCountry:fromCountry,fromCountry:` from `transfers where fromTeamId in 75 123 515 2113 2077f;
update fromCountry:toCountry from `transfers where fromTeamId in 464 12604f;
transfers:select from transfers where season<2016

count 
2# read0`:transfers.csv
`int$"F"$"931.0"

select from transfers where fromTeamName=`Unattached

select from transfers where fromCountry=`

select count i by fromCountry,null fromLeague from 
select first fromTeamName,count i,first fromCountry,count distinct fromCountry,distinct asc season by fromTeamId,fromLeague from transfers where season<2016,not fromTeamId in 464 75 123 515 2113 2077 12604f,fromCountry in exec fromCountry from (select count distinct fromLeague,distinct fromLeague by fromCountry from transfers)where fromLeague>3

select distinct asc season by fromTeamId,fromTeamName from transfers where fromCountry=`$"England",fromLeague=`

select from transfers where fromTeamId=464
select from transfers where fromTeamId=75
select from transfers where fromTeamId=515
select from transfers where fromTeamId=2113
select from transfers where fromTeamId=2077
select from transfers where fromTeamId=12604f
