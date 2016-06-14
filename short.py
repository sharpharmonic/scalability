from controllers.nmx_system.server_support.nmx_server import NMXServer
nmxsrv="10.21.13.238" # 10.21.131.202
nmx = NMXServer(nmxsrv, True)

dm = nmx.gui.DM # hats2
dm.launch() # hats2

cm = dm.Database.CatalogManagement 
cm.openCatalogManagement()
cm.restoreAndActivateCatalog("MYTEST", "C:\\DatabaseBkup\\scalability\\" "NMX74PRMACE2NG20DEV400SER.hzp")
# for some reason the catalog dies and I have to run the following
cm.cmObj.wait_until_open(30, "catalogAdmin~~Window", cm.dmItem)
cm.cmObj.Close.press()
cm.openCatalogManagement()
cm.makeCatalogActive("MYTEST") 






'''
#cm.cmObj.Close.press()
cm.cmObj.wait_until_open(30, "catalogAdmin~~Window", cm.dmItem)
cm.cmObj.Close.press()
cm.cmObj.Close.item.mouseClick()  
try:
    redX = cm.cmObj.item.getDescendantByPath("TitleBar~Catalog Management~,Close~Close~")
    redX.mouseClick()
except: 
    pass

cm.dmObjInstance.Home.startServer() 
'''