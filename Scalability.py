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
with open('scalesettings.yml', 'r') as f:
    parms = yaml.load(f)
nmxsrv = parms['nmxParms']['NMXaddr']
CatalogDirectory = parms['nmxParms']['CatalogPath']
timeoutlimit = parms['nmxParms']['timeout']
ExportSCPath = parms['nmxParms']['exportServiceMapPath']
runs = parms['nmxParms']['numofRun']
Standard = parms['ExpectedTiming']
killall = parms['killalldirectory']
logdirectory = parms['logdirectory']
logbackup = parms['logbackup']

print "inst server"
nmx = NMXServer(nmxsrv, True)

dm = nmx.gui.DM
print "launch domain manager"
dm.launch()

NMXconnect(nmxsrv)  # hats1
designer = Designer()         # hats1
#designer.launch(Passwd="harmonic")  # hats1
#designer = nmx.gui.Designer  # hats2
#designer.launch()               # hats2

'''  needed for monitoring status bar and preventing services from start/stop prematurely '''


def timedelay(x):
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

'''  list of catalogs '''


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
Item = Catalogs()[0].replace("NG", ",NG,").replace("DEV", ',DEV,').replace("SER", ",SER,")
Item2 = Item.split(",")
print Item2[0]  # Type
print Item2[1]  # NG
print Item2[2]  # Dev #
print Item2[3]  # Dev
print Item2[4]  # Service #
print Item2[5]  # Service
print Item2[6]

''' Report '''

report = []


def dev(DTYPE, DEV, SER, StartDMDeact, StopDMDeact, DeactivateSC, ActivateSC):
    return locals()

''' load catalog, first time will need to be upgraded: record start and stop time after upgrade'''


def DomainStart():
    dm.Home.startServer()


def DomainStop():
    dm.Home.stopServer()


def StopDesignerService():
    designer.ServiceView.deactivateService("Site - 1|NG - 1|New Service Plan")


def StartDesignerService():
    designer.ServiceView.activateService("Site - 1|NG - 1|New Service Plan")


def DomainManager(Cat, sc):
    tlist = []
    Item = Cat.replace("NG", ",NG,").replace("DEV", ',DEV,').replace("SER", ",SER,")
    Item2 = Item.split(",")
    name = Item2[0] 
    tlist.append(name)
    Dev = Item2[2] 
    tlist.append("Dev|" + Dev)
    Ser = Item2[4]
    tlist.append("Ser|" + Ser)
    cm = dm.Database.CatalogManagement 
    print "==open catalog"
    cm.openCatalogManagement()
    print "==activate catalog"
    #cm.makeCatalogActive("THETEST")  # THETEST create this new catalog with no devices before running script
    print "==restore catalog"
    #cm.restoreAndActivateCatalog("MYTEST", "C:\\DatabaseBkup\\scalability\\" "NMX73PRMACE2NG20DEV400SER.hzp")
    cm.restoreAndActivateCatalog(name, CatalogDirectory + Cat)  
    print "==stop server"
    dm.Home.stopServer()
    print "get time start"
    t1 = datetime.datetime.now()
    dm.Home.startServer()
    deltastart = datetime.datetime.now() - t1
    tlist.append('StartDM' + sc + "|" + str(deltastart))
    print "Time=%d.%d" % (deltastart.seconds, deltastart.microseconds)
    t2 = datetime.datetime.now()
    print "get time stop"
    dm.Home.stopServer()
    deltastop = datetime.datetime.now() - t2
    tlist.append("StopDM" + sc + "|" + str(deltastop))
    print "Time=%d.%d" % (deltastop.seconds, deltastop.microseconds)
    return tlist


'''  start Deisgner and get service time '''
#  hats1 deprecated, NMXconnect('10.21.11.204'), designer = Designer(), designer.launch(Passwd="harmonic")


def DesignerService():
    tlist = []
    designer.launch(Passwd="harmonic")  # hats1
    #designer = nmx.gui.Designer  # hats2
    print "launch designer"
    #designer.launch()               # hats2
    print "=====deactivate service"

    designer.ServiceView.deactivateService("Site - 1|NG - 1|New Service Plan")
    #timedelay(5)  # hats2

    d1 = datetime.datetime.now()
    print "=====get service start time"
    designer.ServiceView.activateService("Site - 1|NG - 1|New Service Plan")
    #timedelay(20)  # hats2
    time.sleep(10)  # hats1

    d2 = datetime.datetime.now()
    print "=====get service stop time"
    designer.ServiceView.deactivateService("Site - 1|NG - 1|New Service Plan")
    deltastartD = datetime.datetime.now() - d1  # collect time for activated service 1 second after deactivate
    print "Stop Time=%d.%d" % (deltastartD.seconds, deltastartD.microseconds)
    #timedelay(5)  # hats2
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


''' Main Loop '''
#for Cat in Catalogs():
#   DomainManager(Cat)
dmdeact = DomainManager(Catalogs()[0], 'DeactivateSC')
print dmdeact
print "---start server for designer test"
DomainStart()
servicedeact = DesignerService()
Ser = dmdeact[2].split("|")
print Ser
Dev = dmdeact[1].split("|")
print Dev
StartDMD = dmdeact[3].split("|")
print StartDMD
StopDMD = dmdeact[4].split("|")
print StopDMD
print "Start Designer and Activate Service"
StartDesignerService()
dmact = DomainManager(Catalogs()[0], 'ActivateSC')
print "List with active services"
print dmact
DomainStart()
print "Start Designer and Deactivate Service"
StopDesignerService()
print "==================================================================================================="
data = dev(DTYPE=dmdeact[0], DEV=Dev[1], SER=Ser[1], StartDMDeact=StartDMD[1], StopDMDeact=StopDMD[1], 
           DeactivateSC=servicedeact[0], ActivateSC=servicedeact[1])
print data

print "End"
