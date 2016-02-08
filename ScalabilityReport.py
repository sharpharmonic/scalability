
#f=open('C:\\HATSFramework\\logs\\ScalabilityLogTest.out','r')
f=open('C:\\HATSFramework\\logs\\ScalabilityTest2.out','r')
mlist=[]
devicelist=['DTYPE','DEV','SER','StartDMDeact','StartDMAct','StopDMDeact','StopDMAct','ActivateSC','DeactivateSC']
description=['DTYPE','DEV','Number of Services','Start NMX SC Deactivated','Start NMX SC Activated','Stop NMX SC Deactivated','Stop NMX SC Activated','Activating SC','Deactivating SC']
for i in f.readlines():
	dat = eval(i)
	mlist.append(dat)
#print mlist  # for debugging
#dat=[mlist[item]['DTYPE'] for item in range(len(mlist))] # for debugging
#print dat  # for debugging
#print mlist[0]['DTYPE'], ",", mlist[1]['DTYPE']
num=0
for rep in devicelist:
	dat=[mlist[item][rep] for item in range(len(mlist))]  # gen expr example: mlist[0]['DTYPE]
	#print dat
	newdat=str(dat).replace("[","").replace("]","")
	print description[num], "," , newdat
	num+=1
	

