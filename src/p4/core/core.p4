/* -*- P4_16 -*- */
#include <core.p4>
#include <v1model.p4>

#include "egress.p4"
#include "ingress.p4"

V1Switch(
    MyParser(),
    MyIngress(),
    MyEgress(),
    MyDeparser()
) main;
