#!/bin/bash
# 指定authorized_keys的位置
keys="/opt/apps/bastion"
# 创建跳板机镜像
docker build -t ljops/bastion:v1 ljremote
# 开启跳板机，并指定登录用户rsa公钥，方便后续维护。
docker run --name ljops-jumpserver --hostname="jumpserver" -d --restart=always \
-v ${keys}/authorized_keys:/root/.ssh/authorized_keys:ro -p 9022:9022 ljops/bastion:v1
# 检查创建情况。
[ $? -eq 0 ] && echo "Create success!" && exit 1

