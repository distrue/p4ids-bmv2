#include <core.p4>
#include <v1model.p4>

#include "../include/headers.p4"

control MyEgress(
    inout headers hdr,
    inout metadata meta,
    inout standard_metadata_t standard_metadata)
{
    counter((bit<32>)IPV4_ENTRIES, CounterType.packets) packet_freq_cnt;

    apply {
        packet_freq_cnt.count((bit<32>) hdr.ipv4.srcAddr);
    }
}

control MyDeparser(packet_out packet, in headers hdr)
{
    apply {
    	packet.emit(hdr.ethernet);
		packet.emit(hdr.ipv4);
		packet.emit(hdr.tcp);
		packet.emit(hdr.udp);
    }
}