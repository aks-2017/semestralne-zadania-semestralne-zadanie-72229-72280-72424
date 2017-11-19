#!/bin/bash

# The primary network interface
printf '\n# The OpenFlow Switch interfaces\nauto enp6s0\niface enp6s0 inet manual\n\tpre-up ifconfig $IFACE promisc up\n\tpost-down ifconfig $IFACE promisc down\n\nauto enp10s0\niface enp10s0 inet manual\n\tpre-up ifconfig $IFACE promisc up\n\tpost-down ifconfig $IFACE promisc down\n\nauto enp11s0\niface enp11s0 inet manual\n\tpre-up ifconfig $IFACE promisc up\n\tpost-down ifconfig $IFACE promisc down' >> /etc/network/interfaces

# Installation of Open vSwitch and other software for switch_setup.py script usage
apt-get install python-pip openvswitch-switch -y
python -m pip install IPy

# Creation of OF switch and add port to brigde
service openvswitch-switch start
ovs-vsctl add-br of-switch
ovs-vsctl add-port of-switch enp6s0
ovs-vsctl add-port of-switch enp10s0
ovs-vsctl add-port of-switch enp11s0

# Set OF vesion used by switch to 1.0 and 1.3
ovs-vsctl set bridge of-switch protocols=OpenFlow10,OpenFlow13
ovs-ofctl -O OpenFlow10,OpenFlow13 dump-flows of-switch
