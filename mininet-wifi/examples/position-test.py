#!/usr/bin/python

"""
A python program that will set up two stations connected to two access points, and set node positions and radio range 
so that we can see how these properties affect the emulated network. I used the Mininet-WiFi example script 
2AccessPoints.py as the base for the script shown below, then I added the position information to each node and 
enabled association control.
"""

from mininet.net import Mininet
from mininet.node import Controller, OVSKernelSwitch
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel


def topology():

    net = Mininet(controller=Controller, link=TCLink, switch=OVSKernelSwitch)

    print "*** Creating nodes"
    ap1 = net.addAccessPoint('ap1', ssid='ssid-ap1', mode='g', channel='1', position='10,30,0', range='20')
    ap2 = net.addAccessPoint('ap2', ssid='ssid-ap2', mode='g', channel='6', position='50,30,0', range='20')
    sta1 = net.addStation('sta1', mac='00:00:00:00:00:01', ip='10.0.0.1/8', position='10,20,0')
    sta2 = net.addStation('sta2', mac='00:00:00:00:00:02', ip='10.0.0.2/8', position='50,20,0')
    c1 = net.addController('c1', controller=Controller, ip='127.0.0.1', port=6653)

    """plot graph"""
    net.plotGraph(max_x=60, max_y=60)

    # Comment out the following two lines to disable AP
    print "*** Enabling association control (AP)"
    net.associationControl('ssf')

    print "*** Configuring wifi nodes"
    net.configureWifiNodes()

    print "*** Creating links and associations"
    net.addLink(ap1, ap2)
    net.addLink(ap1, sta1)
    net.addLink(ap2, sta2)

    print "*** Starting network"
    net.build()
    c1.start()
    ap1.start([c1])
    ap2.start([c1])

    print "*** Running CLI"
    CLI(net)

    print "*** Stopping network"
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    topology()
