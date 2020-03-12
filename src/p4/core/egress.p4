#include <core.p4>
#include <v1model.p4>

#include "../include/headers.p4"

control MyEgress(
    inout headers hdr,
    inout metadata meta,
    inout stanard_metadata_t stanard_metadata)
{
    counter(BLOCK_ENTRIES, CounterType.packets) packet_freq_cnt;

    apply {
        packet_freq_cnt.count((bit<16>) hdr.ipv4.srcAddr);
    }
}
