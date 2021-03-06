from p4utils.utils.topology import Topology
from p4utils.utils.sswitch_API import SimpleSwitchAPI
from scapy.all import sniff, Packet, Ether, IP, UDP, TCP, BitField, Raw
from crc import Crc

import socket
import threading
import struct
import random

VTABLE_SLOT_SIZE = 8   # in bytes
VTABLE_ENTRIES = 65536

CONTROLLER_MIRROR_SESSION = 100

class NetcacheHeader(Packet):
    name = 'NcachePacket'
    fields_desc = [BitField('op', 0, 8), BitField('seq', 0, 32),
            BitField('key', 0, 128), BitField('value', 0, 512)]


class NCacheController(object):

    def __init__(self, sw_name):
        self.topo = Topology(db="./topology.db")
        self.sw_name = sw_name
        self.thrift_port = self.topo.get_thrift_port(self.sw_name)
        self.cpu_port = self.topo.get_cpu_port_index(self.sw_name)
        self.controller = SimpleSwitchAPI(self.thrift_port)

        self.custom_calcs = self.controller.get_custom_crc_calcs()
        self.sketch_register_num = len(self.custom_calcs)

        self.setup()

    def setup(self):
        if self.cpu_port:
            self.controller.mirroring_add(CONTROLLER_MIRROR_SESSION, self.cpu_port)

    # set a static allocation scheme for l2 forwarding where the mac address of
    # each host is associated with the port connecting this host to the switch
    def set_forwarding_table(self):
        for host in self.topo.get_hosts_connected_to(self.sw_name):
            port = self.topo.node_to_node_port_num(self.sw_name, host)
            host_mac = self.topo.get_host_mac(host)
            print str(host_mac) + str(port)
            self.controller.table_add("l2_forward", "set_egress_port", [str(host_mac)], [str(port)])

    def main(self):
        self.set_forwarding_table()

if __name__ == "__main__":
    controller = NCacheController('s1')
    controller.main()
