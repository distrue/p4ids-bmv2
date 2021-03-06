#include <core.p4>
#include <v1model.p4>

#include "../include/headers.p4"

parser MyParser(
    packet_in packet, 
    out headers hdr, 
    inout metadata meta,
    inout standard_metadata_t standard_metadata) 
{
    state start {
        transition parse_ethernet;
    }

    state parse_ethernet {
        packet.extract(hdr.ethernet);
        transition select(hdr.ethernet.etherType) {
            TYPE_IPV4: parse_ipv4;
            default: accept;
        }
    }

    state parse_ipv4 {
        packet.extract(hdr.ipv4);
        transition select(hdr.ipv4.protocol){
            TYPE_TCP : parse_tcp;
			TYPE_UDP : parse_udp;
            default: accept;
        }
    }

    state parse_tcp {
        packet.extract(hdr.tcp);
		transition accept;
    }

	state parse_udp {
		packet.extract(hdr.udp);
		transition accept;
	}
}

control MyIngress (
    inout headers hdr,
    inout metadata meta,
    inout standard_metadata_t standard_metadata) 
{
    action drop() {
        mark_to_drop(standard_metadata);
    }
    action set_egress_port(bit<9> port) {
        standard_metadata.egress_spec = port;
    }

    table l2_forward {
        key = {
            hdr.ethernet.dstAddr: exact;
        }
        actions = {
            set_egress_port;
            drop;
        }
        size = 1024;
        default_action = set_egress_port;
    }

    action mark_to_block() {
        meta.block = 1;
    }

    table lookup_table {
        key = {
            hdr.ipv4.srcAddr : lpm;
        }
        actions = {
            mark_to_block;
            NoAction;
        }
        size = BLOCK_ENTRIES;
        default_action = NoAction;
    }

    apply {
        // lookup_table.apply();
        // if(hdr.block.isBlock != 1) {
        l2_forward.apply();
        // }
    }
}
