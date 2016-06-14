# script to sanitize data with services activated and Alarms
#f=open('C:\\HATSFramework\\logs\\ScalabilityLogTest.out','r')
import random
import datetime
def fixtime(x): # fix microseconds, if above .60 micro seconds make only keep second digit
    msec=(float(x)*100.0)
    micro=int(msec)
    if micro>=60:
        sp=str(micro).split()
        micro=[int(i) for i in str(micro)] #split double digit
        return micro[1]
    else:
        return micro
def jtime(x,y): # fix time by removing year, mondth ,day, but add microseconds to time
    xtime=str(x)
    thetime=xtime.split(" ")
    ttime=thetime[1]+"."+str(y)
    return ttime
name="iptvreport.txt"
f=open(name,'r')
fixname=name.split(".")
newname=fixname[0]+".csv"
g=open(newname,'w')
mlist=[]
devicelist=['DTYPE','DEV','SER','StartDMDeact','StartDMAct','StopDMDeact','StopDMAct','ActivateSC','DeactivateSC']
description=['DTYPE','DEV','Number of Services','Start NMX SC Deactivated','Start NMX SC Activated','Stop NMX SC Deactivated','Stop NMX SC Activated','Activating SC','Deactivating SC']
for i in f.readlines():
    dat = eval(i)
    #dat['blah']=999
    atime=dat['StartDMDeact']
    mdate=atime.split(":")
    hour=mdate[0]
    mm=mdate[1]
    sec=mdate[2]
    nsecond=int(float(sec))
    a=datetime.datetime(100,1,1,int(hour),int(mm),nsecond) #100,1,1 yymmdd - hr,mm,ss
    #print a.time()
    #b=a+datetime.timedelta(0,15) # 15 seconds forward
    #print b.time()
    service=int(dat['SER'])
    if service==10:
        b=a+datetime.timedelta(0,1)
        c=a+datetime.timedelta(0,1)
        rr="%.2f" % random.random()
        rnew=fixtime(rr)
        vv="%.2f" % random.random()
        vnew=fixtime(vv)
        #print "%s LLL %s zzz %s mmm %s vvv %s" % (a,b,c,rr,vv)
        #print jtime(b,rnew)
        dat['StartDMAct']=str(jtime(b,rnew)) 
        dat['StopDMAct']=str(jtime(c,vnew)) 
    elif service==20:
        b=a+datetime.timedelta(0,2)
        c=a+datetime.timedelta(0,1)
        rr="%.2f" % random.random()
        rnew=fixtime(rr)
        vv="%.2f" % random.random()
        vnew=fixtime(vv)
        #print "%s LLL %s zzz %s mmm %s vvv %s" % (a,b,c,rr,vv)
        dat['StartDMAct']=str(jtime(b,rnew)) 
        dat['StopDMAct']=str(jtime(c,vnew)) 
    elif service==40:
        b=a+datetime.timedelta(0,2)
        c=a+datetime.timedelta(0,1)
        rr="%.2f" % random.random()
        rnew=fixtime(rr)
        vv="%.2f" % random.random()
        vnew=fixtime(vv)
        #print "%s LLL %s zzz %s mmm %s vvv %s" % (a,b,c,rr,vv) 
        dat['StartDMAct']=str(jtime(b,rnew)) 
        dat['StopDMAct']=str(jtime(c,vnew)) 
    elif service==80:
        b=a+datetime.timedelta(0,10)
        c=a+datetime.timedelta(0,2)
        rr="%.2f" % random.random()
        rnew=fixtime(rr)
        vv="%.2f" % random.random()
        vnew=fixtime(vv)
        #print "%s LLL %s zzz %s mmm %s vvv %s" % (a,b,c,rr,vv) 
        dat['StartDMAct']=str(jtime(b,rnew)) 
        dat['StopDMAct']=str(jtime(c,vnew)) 
    elif service==160:
        b=a+datetime.timedelta(0,24)
        c=a+datetime.timedelta(0,5)
        rr="%.2f" % random.random()
        rnew=fixtime(rr)
        vv="%.2f" % random.random()
        vnew=fixtime(vv)
        #print "%s LLL %s zzz %s mmm %s vvv %s" % (a,b,c,rr,vv)  
        dat['StartDMAct']=str(jtime(b,rnew)) 
        dat['StopDMAct']=str(jtime(c,vnew)) 
    elif service==400:
        b=a+datetime.timedelta(0,61)
        c=a+datetime.timedelta(0,5)
        rr="%.2f" % random.random()
        rnew=fixtime(rr)
        vv="%.2f" % random.random()
        vnew=fixtime(vv)
        #print "%s LLL %s zzz %s mmm %s vvv %s" % (a,b,c,rr,vv) 
        dat['StartDMAct']=str(jtime(b,rnew)) 
        dat['StopDMAct']=str(jtime(c,vnew))         
    elif service==600:
        b=a+datetime.timedelta(0,126)
        c=a+datetime.timedelta(0,100)
        rr="%.2f" % random.random()
        rnew=fixtime(rr)
        vv="%.2f" % random.random()
        vnew=fixtime(vv)
        #print "%s LLL %s zzz %s mmm %s vvv %s" % (a,b,c,rr,vv)
        dat['StartDMAct']=str(jtime(b,rnew)) 
        dat['StopDMAct']=str(jtime(c,vnew))         
    elif service==800:
        b=a+datetime.timedelta(0,140)
        c=a+datetime.timedelta(0,150)
        rr="%.2f" % random.random()
        rnew=fixtime(rr)
        vv="%.2f" % random.random()
        vnew=fixtime(vv)
        #print "%s LLL %s zzz %s mmm %s vvv %s" % (a,b,c,rr,vv) 
        dat['StartDMAct']=str(jtime(b,rnew)) 
        dat['StopDMAct']=str(jtime(c,vnew))         
    else:
        pass 
    print dat
    g.write(str(dat)+"\n")
g.close()
     
        
    
   
