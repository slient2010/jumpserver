#!/bin/ash
set -x
set -e

# install rpyc
git clone https://github.com/tomerfiliba/rpyc.git
cd rpyc
python setup.py build
python setup.py install
cd ..
rm -rf rpyc
# install paramiko
wget http://172.16.66.13/softwares/setuptools-27.3.0.tar.gz
tar zxf setuptools-27.3.0.tar.gz
cd setuptools-27.3.0
python setup.py build
python setup.py install
cd ..
rm -rf setuptools-27.3.0 setuptools-27.3.0.tar.gz

# install paramiko
wget http://172.16.66.13/softwares/paramiko-2.0.2.tar.gz
tar zxf paramiko-2.0.2.tar.gz
cd paramiko-2.0.2
python setup.py build
python setup.py install
cd ..
rm -rf paramiko-2.0.2 paramiko-2.0.2.tar.gz

# Remove all but a handful of admin commands.
find /sbin /usr/sbin ! -type d \
  -a ! -name sshd \
  -a ! -name nologin \
  -delete

sysdirs="
  /bin
  /etc
  /lib
  /sbin
  /usr
"

# Ensure system dirs are owned by root and not writable by anybody else.
find $sysdirs -xdev -type d \
  -exec chown root:root {} \; \
  -exec chmod 0755 {} \;

# Remove unnecessary user accounts, including root.
sed -i -r '/^(root|dev|sshd)/!d' /etc/group
sed -i -r '/^(root|dev|sshd)/!d' /etc/passwd

# Remove apk configs.
find $sysdirs -xdev -regex '.*apk.*' -exec rm -fr {} +

# Remove crufty...
#   /etc/shadow-
#   /etc/passwd-
#   /etc/group-
find $sysdirs -xdev -type f -regex '.*-$' -exec rm -f {} +

# give permission to ssh key files
chmod 644 /etc/ssh/ssh_*
chmod 600 /etc/ssh/ssh_host_dsa_key
chmod 600 /etc/ssh/ssh_host_rsa_key
chmod 600 /etc/ssh/ssh_host_ecdsa_key
chmod 600 /etc/ssh/ssh_host_ed25519_key

# Remove all suid files.
find $sysdirs -xdev -type f -a -perm +4000 -delete

# Remove other programs that could be dangerous.
find $sysdirs -xdev \( \
  -name hexdump -o \
  -name chgrp -o \
  -name chmod -o \
  -name chown -o \
  -name ln -o \
  -name od -o \
  -name strings -o \
  -name su \
  \) -delete

# Remove init scripts since we do not use them.
rm -fr /etc/init.d
rm -fr /lib/rc
rm -fr /etc/conf.d
rm -fr /etc/inittab
rm -fr /etc/runlevels
rm -fr /etc/rc.conf

# Remove kernel tunables since we do not need them.
rm -fr /etc/sysctl*
rm -fr /etc/modprobe.d
rm -fr /etc/modules
rm -fr /etc/mdev.conf
rm -fr /etc/acpi

# Remove root homedir since we do not need it.
# rm -fr /root

# Remove fstab since we do not need it.
rm -f /etc/fstab

# Remove broken symlinks (because we removed the targets above).
find $sysdirs -xdev -type l -exec test ! -e {} \; -delete

# Remove all but a handful of admin commands.
find /usr/bin /bin ! -type d \
  -a ! -name sh \
  -a ! -name bash \
  -a ! -name ash \
  -a ! -name ssh \
  -a ! -name python \
  -a ! -name python2 \
  -a ! -name python2.7 \
  -a ! -name busybox \
  -delete
