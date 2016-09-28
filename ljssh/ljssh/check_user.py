#!/usr/bin/python
# -*- coding:utf-8 -*-
# 
# 说明： 客户端，集成到web或者独立使用。
# 
# 

import sys
import rpyc
from libs.libraries import *
from config import *

def getServerInfo(userName, hosts):
	try:
		# paramters host, port
		conn =rpyc.connect(SERVER, PORT)
		# 是服务端的那个以"exposed_"开头的方法
		cResult =conn.root.login("%s" % USER, "%s" % PASSWD)	
	except Exception, e:
		cResult = False
		print 'Connect to rpyc server error:' + str(e)
		sys.exit()
	    # logger.error('Connect to rpyc server error:' + str(e))
	    # return HttpResponse('Connect to rpyc server error:' + str(e))
	# 对请求数据串使用m_encode方法加密

	put_string="%s@@%s" % (userName, hosts)
	
	put_string = m_encode(put_string, SECRET_KEY)
	if cResult:
		# 调用rpyc Server的Runcommands方法实现功能模块的任务下发，返回结果使用m_decode进行解密
		try:
			cResult =m_decode(conn.root.Runcommands(put_string), SECRET_KEY)
			return cResult
		except Exception,e:
			print "秘钥异常，或是%s" % e
		conn.close()
	else:
		print "用户验证失败，请重试！"

def makeConnection(userName, hosts, publickeys):
	try:
		# paramters host, port
		conn =rpyc.connect(SERVER, PORT)
		# 是服务端的那个以"exposed_"开头的方法
		cResult =conn.root.login("%s" % USER, "%s" % PASSWD)	
	except Exception, e:
		cResult = False
		print 'Connect to rpyc server error:' + str(e)
		sys.exit()
	# 对请求数据串使用m_encode方法加密
	put_string="%s@@%s@@%s" % (userName, hosts, publickeys)
	
	put_string = m_encode(put_string, SECRET_KEY)
	if cResult:
		# 调用rpyc Server的Runcommands方法实现功能模块的任务下发，返回结果使用m_decode进行解密
		try:
			cResul = m_decode(conn.root.Passpublickeys(put_string), SECRET_KEY)
			return cResul
		except Exception,e:
			print "秘钥异常，或是%s" % e
		conn.close()
	else:
		print "用户验证失败，请重试！"


if __name__ == "__main__":
    username = sys.argv[1]
    ipadd = sys.argv[2]
    check_result = getServerInfo(username, ipadd)
    f = open("/home/%s/.ssh/id_rsa.pub" % username, "r")
    publickeys = f.read()
    makeConnection(username, ipadd, publickeys)
