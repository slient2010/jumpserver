#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import time
import MySQLdb
import paramiko

class Modulehandle():
    def __init__(self, sys_param_row): # 初始化方法
        self.Runresult = ""
        self.sys_param_row = sys_param_row
        self.remote_user = self.sys_param_row['user']
        self.remote_ip = self.sys_param_row['ip']
        # self.hosts = target_host(hosts, "IP")

    def grant_privileges(self, remote_user, remote_ip, keys):
        self.remote_user = remote_user 
        self.remote_ip = remote_ip
        self.remote_keys = keys
        self.port = 22

        command = 'useradd %s ; mkdir -p /home/%s/.ssh ; echo %s >> /home/%s/.ssh/authorized_keys; \
                   chown -R %s.%s /home/%s; chmod 600 /home/%s/.ssh/authorized_keys; \
                   echo "%s ALL=(ALL)	NOPASSWD: ALL" >> /etc/sudoers' % (self.remote_user, \
                   self.remote_user, self.keys, self.remote_user, self.remote_user, \
                   self.remote_user, self.remote_user, self.remote_user, self.remote_user)
        pssh = paramiko.SSHClient()
        pssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        pssh.connect("%s" % remote_ip, self.port,"root")
        stdin, stdout, stderr = pssh.exec_command(" %s " % command)
        pssh.close()

        return stdout.readlines()



    def query(self):
        #连接    
        conn=MySQLdb.connect(host="localhost",user="root",passwd="",db="devops",charset="utf8")  
        cursor = conn.cursor()    
        #查询    
        sql  = 'select name, hosts, created, rsa_key, time from user where name="%s"' % self.remote_user
        
        cursor.execute(sql)
        result = cursor.fetchall()
        if result:
            data = result[0]
            username = data[0]
            host = data[1]
            self.keys = data[3]
            hosts = list(host.strip("\n").split(','))
            new_hosts = str(hosts).replace("u'","\"").replace(r"\n","").replace("'", "\"")
            hts  = list(eval(new_hosts))
            servers = ""
            ips = []
            for i in range(0, len(hts)):
                # a.append(str(hts[i]))
                servers = str(hts[i]) + "@" + servers
                ips.append(str(hts[i]))
            
            times  = data[4]
           #for i in range(len(ips)):
           #    print ips[i]
           #    self.grant_privileges(username, ips[i], self.keys)
        else:
            username = ""
            servers = ""
            times  = ""

        #times  = cursor.fetchall()[0][0]
        cursor.close()    
        #提交    
        conn.commit()
        #关闭    
        conn.close()   
         
#        print "%s, %s, %s" % (self.remote_user, self.remote_ip, self.keys)
        return "%s##%s##%s" %(username, servers, times)
        

    def getinfo(self):
        if self.remote_user == '':
            self.Runresult = "no user"
        elif self.remote_ip == '':
            self.Runresult = "no user"
        else:
            self.Runresult = self.query()
         
       #try:
       #    self.Runresult = "un_20150424_01_gbk.zip@@un_20150427_01_gbk.zip@@un_20150427_01_gbk.zip"
       #except Exception,e:
       #     return str(e)
        # 返回执行结果
        # return self.Runresult  "sss"
        return self.Runresult
