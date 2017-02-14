#!/usr/bin/env python
from mininet.net import Mininet
from mininet.node import Controller, RemoteController
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import Link, Intf, TCLink
from mininet.topo import Topo
from mininet.util import dumpNodeConnections
import logging
import os

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger( __name__ )
pod = 4 #specify the pod number to build the DCN topology
#class to build core, aggregate, edge switches and hosts.
class HugeTopo(Topo):
    logger.debug("Class HugeTopo")
    CoreSwitchList = []
    AggSwitchList = []
    EdgeSwitchList = []
    HostList = []
    iNUMBER = 0
    def __init__(self):
        logger.debug("Class HugeTopo init")
        iNUMBER = pod
#create switches and hosts based on fattree architecture 
        self.iNUMBER = iNUMBER
        self.iCoreLayerSwitch = (iNUMBER/2)**2
        self.iAggLayerSwitch = (iNUMBER**2 /2)
        self.iEdgeLayerSwitch = (iNUMBER**2 /2)
        self.iHost = self.iCoreLayerSwitch * iNUMBER
        #Init Topo
        Topo.__init__(self)
#creating the topology
    def createTopo(self):
        logger.debug("Start create Core Layer Swich")
        self.createCoreLayerSwitch(self.iCoreLayerSwitch)
        logger.debug("Start create Agg Layer Swich ")
        self.createAggLayerSwitch(self.iAggLayerSwitch)
        logger.debug("Start create Edge Layer Swich ")
        self.createEdgeLayerSwitch(self.iEdgeLayerSwitch)
        logger.debug("Start create Host")
        self.createHost(self.iHost)

    """
    Create Switch and Host
    """
#create core switch
    def createCoreLayerSwitch(self, NUMBER):
        logger.debug("Create Core Layer")
        for x in range(1, NUMBER+1):
            PREFIX = "100"
            if x >= int(10):
                PREFIX = "10"
            self.CoreSwitchList.append(self.addSwitch(PREFIX + str(x)))
#create aggregate switch
    def createAggLayerSwitch(self, NUMBER):
        logger.debug( "Create Agg Layer")
        for x in range(1, NUMBER+1):
            PREFIX = "200"
            if x >= int(10):
                PREFIX = "20"
            self.AggSwitchList.append(self.addSwitch(PREFIX + str(x)))
#create edge switch
    def createEdgeLayerSwitch(self, NUMBER):
        logger.debug("Create Edge Layer")
        for x in range(1, NUMBER+1):
            PREFIX = "300"
            if x >= int(10):
                PREFIX = "30"
            self.EdgeSwitchList.append(self.addSwitch(PREFIX + str(x)))
#create hosts
    def createHost(self, NUMBER):
        logger.debug("Create Host")
        for x in range(1, NUMBER+1):
            PREFIX = "400"
            if x >= int(10):
                PREFIX = "40"
            self.HostList.append(self.addHost(PREFIX + str(x)))

    """
    Create Link
    """
    def createLink(self):
        logger.debug("Create Core to Agg")
        for x in range(0, self.iAggLayerSwitch, self.iNUMBER/2):
			for y in range(0,self.iNUMBER/2,1):
				for z in range(0,self.iNUMBER/2,1):
					self.addLink(self.CoreSwitchList[y+z*self.iNUMBER/2], self.AggSwitchList[x+z])
			
        logger.debug("Create Agg to Edge")
        for x in range(0, self.iAggLayerSwitch,self.iNUMBER/2):
			for y in range(0,self.iNUMBER/2,1):
				for z in range(0,self.iNUMBER/2,1):
					self.addLink(self.AggSwitchList[x+z], self.EdgeSwitchList[x+y])
				
          
        logger.debug("Create Edge to Host")
        for x in range(0, self.iEdgeLayerSwitch):
			for y in range(0,self.iNUMBER/2,1):
				self.addLink(self.EdgeSwitchList[x], self.HostList[self.iNUMBER*x/2+y])
#enabling the spanning tree protocol
def enableSTP():
   #for core switches
    for x in range(1,(pod/2)**2+1):
        cmd = "ovs-vsctl set Bridge %s stp_enable=true" % (str(1000+x))
        os.system(cmd)
        print cmd
#for edge and aggregate switches
    for x in range(1,pod**2/2+1):
        cmd = "ovs-vsctl set Bridge %s stp_enable=true" % (str(2000+x))
        os.system(cmd)
        print cmd
        cmd = "ovs-vsctl set Bridge %s stp_enable=true" % (str(3000+x))
        os.system(cmd)
        print cmd
		
		#IP Subnetting tenant arrangement
def Host_Interface_IP(net, topo):
   logger.debug("Start Host_Interface_IP Configurations")
  
   h1001, h1002, h1003, h1004, h1005, h1006, h1007, h1008, h1009, h1010, h1011, h1012, h1013, h1014, h1015, h1016 = net.get(topo.HostList[0], topo.HostList[1], topo.HostList[2], topo.HostList[3], topo.HostList[4], topo.HostList[5], topo.HostList[6], topo.HostList[7], topo.HostList[8], topo.HostList[9], topo.HostList[10], topo.HostList[11], topo.HostList[12], topo.HostList[13], topo.HostList[14], topo.HostList[15])
   h1001.cmdPrint('ifconfig 4001-eth0 10.0.0.1 netmask 255.255.255.248')
   h1005.cmdPrint('ifconfig 4005-eth0 10.0.0.2 netmask 255.255.255.248')
   h1009.cmdPrint('ifconfig 4009-eth0 10.0.0.3 netmask 255.255.255.248')
   h1013.cmdPrint('ifconfig 4013-eth0 10.0.0.4 netmask 255.255.255.248')

   h1002.cmdPrint('ifconfig 4002-eth0 10.0.0.9 netmask 255.255.255.248')
   h1006.cmdPrint('ifconfig 4006-eth0 10.0.0.10 netmask 255.255.255.248')
   h1010.cmdPrint('ifconfig 4010-eth0 10.0.0.11 netmask 255.255.255.248')
   h1014.cmdPrint('ifconfig 4014-eth0 10.0.0.12 netmask 255.255.255.248')

   h1003.cmdPrint('ifconfig 4003-eth0 10.0.0.17 netmask 255.255.255.248')
   h1007.cmdPrint('ifconfig 4007-eth0 10.0.0.18 netmask 255.255.255.248')
   h1011.cmdPrint('ifconfig 4011-eth0 10.0.0.19 netmask 255.255.255.248')
   h1015.cmdPrint('ifconfig 4015-eth0 10.0.0.20 netmask 255.255.255.248')

   h1004.cmdPrint('ifconfig 4004-eth0 10.0.0.25 netmask 255.255.255.248')
   h1008.cmdPrint('ifconfig 4008-eth0 10.0.0.26 netmask 255.255.255.248')
   h1012.cmdPrint('ifconfig 4012-eth0 10.0.0.27 netmask 255.255.255.248')
   h1016.cmdPrint('ifconfig 4016-eth0 10.0.0.28 netmask 255.255.255.248')

#creating the topology in mininet
def createTopo():
    logging.debug("LV1 Create HugeTopo")
    topo = HugeTopo()
    topo.createTopo()
    topo.createLink()

    logging.debug("LV1 Start Mininet")
    CONTROLLER_IP = "127.0.0.1"
    CONTROLLER_PORT = 6633
    net = Mininet(topo=topo, link=TCLink, controller=None)
    net.addController( 'controller',controller=RemoteController,ip=CONTROLLER_IP,port=CONTROLLER_PORT)
    net.start()
    logger.debug("LV1 dumpNode")
    enableSTP()
    dumpNodeConnections(net.hosts)
	Host_Interface_IP(net, topo)
    CLI(net)
    net.stop()
if __name__ == '__main__':
    setLogLevel('info')
    if os.getuid() != 0:
        logger.debug("You are NOT root")
    elif os.getuid() == 0:
        createTopo()


