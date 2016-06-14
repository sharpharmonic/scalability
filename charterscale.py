'''
Created on Oct 5, 2015

@author: wgunnell
'''
#  HATS 2
import time
from controllers.nmx_system.server_support.nmx_server import NMXServer
import yaml
import datetime
import os

#  HATS 1
from NMX import NMXconnect
from NMX7.Designer import Designer

''' global '''


print "read scalesettings.yml"
'''
with open('scalesettings.yml', 'r') as f:
    parms = yaml.load(f)
#nmxsrv = parms['nmxParms']['NMXaddr']
CatalogDirectory = parms['nmxParms']['CatalogPath']
timeoutlimit = parms['nmxParms']['timeout']
ExportSCPath = parms['nmxParms']['exportServiceMapPath']
runs = parms['nmxParms']['numofRun']
Standard = parms['ExpectedTiming']
killall = parms['killalldirectory']
logdirectory = parms['logdirectory']
logbackup = parms['logbackup']
'''

print "inst server"
nmxsrv="10.21.13.238"
#nmx = NMXServer(nmxsrv, True) # hats2
nmx = NMXServer(nmxsrv) # hats2
dm = nmx.gui.DM # hats2
print "launch domain manager"
dm.launch(UserID='jrodgers', Passwd='P@55w0rd') # hats2

#NMXconnect(nmxsrv)  # hats1
#nmx=NMXServer()
#from NMX import DM # hats1
#dm=nmx.DM() # hats1
#dm=DM()
#dm.launch() # hats1


#designer = Designer()         # hats1
#designer.launch(Passwd="harmonic")  # hats1
#designer = nmx.gui.Designer  # hats2
#designer.launch()               # hats2
#needed for monitoring status bar and preventing services from start/stop prematurely


def timedelay(x,designer):
    for i in range(1, x):
        time.sleep(1)
        statusItem = designer.item.getDescendantByPath("statusBar~~StatusBar,statusReady~~StatusBarItem,~~TextBlock")
        status = statusItem.HLAname
        print status, " ", i
        if 'Provision' in str(status):
            time.sleep(10)
            print "10 seconds: %s" % status
            break
        else:
            time.sleep(1)
            statusItem = ''
            status = ''

#list of catalogs


def Catalogs():
    listcat = []
    for i in nmx.dirList(CatalogDirectory):
        if 'NMX' in i:  # ignore other files
            #print i
            listcat.append(i)
    #print listcat
    return listcat

print Catalogs()[0]
name = Catalogs()[0].split('.')
print name[0]
'''
Item = Catalogs()[0].replace("NG", ",NG,").replace("DEV", ',DEV,').replace("SER", ",SER,")
Item2 = Item.split(",")
print Item2[0]  # Type
print Item2[1]  # NG
print Item2[2]  # Dev #
print Item2[3]  # Dev
print Item2[4]  # Service #
print Item2[5]  # Service
print Item2[6]
'''
#Report

report = []


def dev(DTYPE, DEV, SER, StartDMDeact, StopDMDeact, DeactivateSC, ActivateSC):
    return locals()

#load catalog, first time will need to be upgraded: record start and stop time after upgrade


def DomainStart():
    try:
        dm.Home.startServer()
    except:
        print "tried to start domain manager - try again"
        time.sleep(10)
        try:
            dm.Home.startServer()
        except:
            print "still coudln't start domain manager - no worries catalog needs upgrade anyways"
            pass

def DomainStop():
    try:
        dm.Home.stopServer()
    except:
        print "for some strange reason it would not stop"
        pass
        

def DomainManager(Cat, sc):
    tlist = []
    #Item = Cat.replace("NG", ",NG,").replace("DEV", ',DEV,').replace("SER", ",SER,")
    #Item2 = Item.split(",")
    #name = Item2[0] 
    name="Charter"
    tlist.append(name)
    #Dev = Item2[2] 
    Dev=10
    tlist.append("Dev|" + Dev)
    #Ser = Item2[4]
    Ser=6308
    tlist.append("Ser|" + Ser)
    cm = dm.Database.CatalogManagement 
    print "==open catalog"
    try:
        print "if domain manager is stuck on starting. Click to close it"
        cm.openCatalogManagement()
        try:
            time.sleep(10)
            cm.openCatalogManagement()
        except:
            print "catalog won't start - "
    except:
        print "oooops"
    print "==activate catalog"
    #cm.makeCatalogActive("THETEST")  # THETEST create this new catalog with no devices before running script
    print "==restore catalog"
    #cm.restoreAndActivateCatalog("MYTEST", "C:\\DatabaseBkup\\scalability\\" "NMX73PRMACE2NG20DEV400SER.hzp")
    try:
        cm.restoreAndActivateCatalog(name, CatalogDirectory + "\\" + Cat)  
    except:
        print "not sure why it can't restore sleep 300"
        try:
            time.sleep(330)
            #cm.restoreAndActivateCatalog(name, CatalogDirectory + "\\" + Cat)
            cm.cmObj.wait_until_open(30, "catalogAdmin~~Window", cm.dmItem)
            cm.cmObj.Close.press()
            cm.openCatalogManagement()
            cm.makeCatalogActive(name) 
        except:
            print "trying after 330s"
            pass
            '''
            try:
                time.sleep(180)
                cm.restoreAndActivateCatalog(name, CatalogDirectory + "\\" + Cat)
            except:
                print "still taking too long"
                try:
                    print "not working close anyways"
                    cm.cmObj.Close.press()
                    try:
                        cmObj.Close.item.mouseClick() 
                    except:
                        print "mouse click error"
                        pass
                except:
                    print "missed click"
                    pass
            '''
    print "==stop server"
    dm.Home.stopServer()
    print "get time start"
    t1 = datetime.datetime.now()
    try:
        dm.Home.startServer()
    except:
        pass
    deltastart = datetime.datetime.now() - t1
    tlist.append('StartDM' + sc + "|" + str(deltastart))
    print "Time=%d.%d" % (deltastart.seconds, deltastart.microseconds)
    t2 = datetime.datetime.now()
    print "get time stop"
    try:
        dm.Home.stopServer()
    except:
        print "TimeLimitError Waited for 3 mintues for DM Server"
        time.sleep(60)
        try:
            dm.Home.stopServer()
        except:
            print "waited additional 60 seconds"
            pass
    deltastop = datetime.datetime.now() - t2
    tlist.append("StopDM" + sc + "|" + str(deltastop))
    print "Time=%d.%d" % (deltastop.seconds, deltastop.microseconds)
    try:
        print "closing catalog screen just in case"
        cm.cmObj.Close.press()
    except:
        print "failed to close catalog screen at the end"
        pass
    return tlist


#start Deisgner and get service time
#  hats1 deprecated, NMXconnect('10.21.11.204'), designer = Designer(), designer.launch(Passwd="harmonic")


def DesignerService(D):
    tlist = []
    #designer.launch(Passwd="harmonic")  # hats1
    #designer = nmx.gui.Designer  # hats2 # move out into main
    #print "launch designer"
    #designer.launch()               # hats2
    print "=====deactivate service"

    #designer.ServiceView.deactivateService("Site - 1|NG - 1|New Service Plan")
    D.ServiceView.select("Site - 1|NG - 1|New Service Plan")
    D.FlowView.deactivateService("Site - 1|NG - 1|New Service Plan")
    #timedelay(5,D)  # hats2
    time.sleep(5)
    
    d1 = datetime.datetime.now()
    print "=====get service start time"
    #designer.ServiceView.activateService("Site - 1|NG - 1|New Service Plan")
    D.FlowView.activateService("Site - 1|NG - 1|New Service Plan")
    #imedelay(20,D)  # hats2
    time.sleep(10)  # hats1

    d2 = datetime.datetime.now()
    print "=====get service stop time"
    #designer.ServiceView.deactivateService("Site - 1|NG - 1|New Service Plan")
    D.FlowView.deactivateService("Site - 1|NG - 1|New Service Plan")
    deltastartD = datetime.datetime.now() - d1  # collect time for activated service 1 second after deactivate
    print "Stop Time=%d.%d" % (deltastartD.seconds, deltastartD.microseconds)
    #timedelay(5,D)  # hats2
    time.sleep(10)  # hats1

    deltastopD = datetime.datetime.now() - d2
    print "=====Report ====="
    print "Start Services Time=%d.%d" % (deltastartD.seconds, deltastartD.microseconds)
    print "Stop Services Time=%d.%d" % (deltastopD.seconds, deltastopD.microseconds)
    print "==hello at the end script complete"  
    sstart = "%d.%d" % (deltastartD.seconds, deltastartD.microseconds)
    sstop = "%d.%d" % (deltastopD.seconds, deltastopD.microseconds)
    tlist.append(sstart)
    tlist.append(sstop)
    return tlist

def StopDesignerService(D):
    #designer.ServiceView.deactivateService("Site - 1|NG - 1|New Service Plan")
    try:
        D.FlowView.deactivateService("Site - 1|NG - 1|New Service Plan")
    except:
        print "couldn't stop designer service single function"
        pass 
        
def StartDesignerService(D):
    #designer.ServiceView.activateService("Site - 1|NG - 1|New Service Plan")
    try:
        D.FlowView.activateService("Site - 1|NG - 1|New Service Plan")
    except:
        print "coudn't start designer service single function"
        pass

if __name__=="__main__":
           
     
        #Main Loop
        #for Cat in Catalogs():
        f=open("CharterReport.txt","a")   
        #DomainManager(Cat)
        dmdeact = DomainManager(Catalogs()[0], 'DeactivateSC')
        #dmdeact = DomainManager(Cat, 'DeactivateSC')
        print dmdeact
        print "---start server for designer test"
        DomainStart()
        designer = nmx.gui.Designer # launch designer
        print "launch designer"     # launch designer
        try:
            designer.launch(UserID='jrodgers', Passwd='P@55w0rd')           # launch designer
        except:
            print "slow to launch designer But will pass just in case it did"
            time.sleep(10)
            pass
        try:
            servicedeact = DesignerService(designer)
        except:
            print "couldn't start service again"
            try:
                
                print "launch designer again"     # launch designer
               
                servicedeact = DesignerService(designer)
            except:
                print "blaaaaa"
                pass
        Ser = dmdeact[2].split("|")
        print Ser
        Dev = dmdeact[1].split("|")
        print Dev
        StartDMD = dmdeact[3].split("|")
        print StartDMD
        StopDMD = dmdeact[4].split("|")
        print StopDMD
        print "Start Designer and Activate Service"
        StartDesignerService(designer)
        #dmact = DomainManager(Catalogs()[0], 'ActivateSC')
        dmact = DomainManager(Cat, 'ActivateSC')
        print "List with active services"
        print dmact
        DomainStart()
        print "Start Designer and Deactivate Service"
        time.sleep(10)
        try:
            StopDesignerService(designer)
        except:
            print "couldn't StopDesignerService"
            time.sleep(10)
            try:
                StopDesignerService(designer)
            except:
                print "couldn't stop again - continue with reporting"
        print "==================================================================================================="
        data = dev(DTYPE=dmdeact[0], DEV=Dev[1], SER=Ser[1], StartDMDeact=StartDMD[1], StopDMDeact=StopDMD[1], 
                   DeactivateSC=servicedeact[0], ActivateSC=servicedeact[1])
        print data
        f.write(str(data))
        f.close()
        print "End"
        
        
        
        
        
        

