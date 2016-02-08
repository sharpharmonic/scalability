
#f=open('C:\\HATSFramework\\logs\\ScalabilityLogTest.out','r')
f=open('C:\\HATSFramework\\logs\\ScalabilityLog.out','r')
mlist=[]
devicelist=['DTYPE','DEV','SER','StartDMDeact','StopDMDeact','DeactivateSC','ActivateSC','StartDMAct','StopDMAct']
for i in f.readlines():
	dat = eval(i)
	#print dat
	#print type(dat)
	#print dat['DTYPE']
	mlist.append(dat)

print " list=================="
#print mlist  # for debugging
dat=[mlist[item]['DTYPE'] for item in range(len(mlist))]
#print dat  # for debugging
#print mlist[0]['DTYPE'], ",", mlist[1]['DTYPE']
for rep in devicelist:
	dat=[mlist[item][rep] for item in range(len(mlist))]  # gen expr example: mlist[0]['DTYPE]
	print dat
