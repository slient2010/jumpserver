#!/bin/bash

keys="/opt/ljops/apps/bastion"
docker build -t ljops/bastion:v1 ljremote
docker run --name ljops-jumpserver --hostname="jumpserver" -d --restart=always -v ${keys}/authorized_keys:/home/dev/.ssh/authorized_keys:ro -v ${keys}/authorized_keys:/root/.ssh/authorized_keys:ro -p 9022:9022 ljops/bastion:v1
[ $? -eq 0 ] && echo "Create success!" && exit 1

