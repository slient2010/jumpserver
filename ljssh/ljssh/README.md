### 使用说明

1.将该文件夹存放在跳板机的：/opt/ljops/apps/目录中（若无则手动创建，使用root账号：busybox mkdir -p /opt/ljops/apps）

2.修改config.py中服务器地址

3.替换ssh 
busybox mv /usr/bin/ssh /usr/bin/ljssh
busybox ln -s /opt/ljops/apps/ljssh/ssh /usr/bin/ssh

4.添加需要使用该跳板机的账户

举例子：使用账号test

busybox adduser test -D

busybox passwd -d test

生成该账号的rsa秘钥对，方便后续登录授权服务器。

busybox mkdir /home/test/.ssh

busybox chown test -R /home/test/.ssh

python /opt/ljops/apps/ljssh/gen_key.py test





