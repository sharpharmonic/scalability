import time
from controllers.nmx_system.server_support.nmx_server import NMXServer
import yaml
import datetime
import os
from NMX import NMXconnect
from NMX7.Designer import Designer

NMXconnect('10.21.11.204')
designer = Designer()   
designer.launch(Passwd="harmonic")

print designer.item.ID
statusItem=designer.item.getDescendantByPath("statusBar~~StatusBar,statusReady~~StatusBarItem,~~TextBlock")
print statusItem.ID
status = statusItem.HLAname
print status
