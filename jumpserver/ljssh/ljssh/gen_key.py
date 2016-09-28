#!/usr/bin/python
#-*-coding:utf8-*-

import os
import StringIO
from paramiko import *
import sys

def gen_keys(key="", username="root"):
    """
    生成公钥 私钥
    """
    output = StringIO.StringIO()
    sbuffer = StringIO.StringIO()
    key_content = {}
    if not key:
        try:
            key = RSAKey.generate(2048)
            key.write_private_key(output)
            private_key = output.getvalue()
        except IOError:
            raise IOError('gen_keys: there was an error writing to the file')
        except SSHException:
            raise SSHException('gen_keys: the key is invalid')
    else:
        private_key = key
        output.write(key)
        try:
            key = RSAKey.from_private_key(output)
        except SSHException, e:
            raise SSHException(e)

    for data in [key.get_name(),
                 " ",
                 key.get_base64(),
                 " %s@%s" % (username, os.uname()[1])]:
        sbuffer.write(data)
    public_key = sbuffer.getvalue()
    key_content['public_key'] = public_key
    key_content['private_key'] = private_key
    return key_content

if __name__ == "__main__":
    if len(sys.argv) == 2:
        username = sys.argv[1]
    else:
        sys.exit()
#    if len(sys.argvs)

    gen = gen_keys(username ="%s" % username)
    f = open("/home/%s/.ssh/id_rsa.pub" % username, "w")
    f.write(gen['public_key'])
    f.close()

    f = open("/home/%s/.ssh/id_rsa" % username, "w")
    f.write(gen['private_key'])
    f.close()


