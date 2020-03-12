#!/bin/sh

ROOT_DIR=../

PYTHON="python3"

usage="${0} <n_servers> [<server-init-flags>]"

n_servers=$1
server_flags=$2

if [ -z $n_servers ]; then
	echo "Error: invalid input: ${usage}"
	exit 1
fi


for i in $(seq $n_servers); do
	mx server$i $PYTHON $NCACHE_DIR/src/server/server.py $server_flags &
done
