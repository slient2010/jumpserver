# Docker 机器作为跳板机。


## 约定： 
`
   文件目录为：/opt/apps/bastion
`
## 使用方法：    
1. 创建 `authorized_keys` 文件用来存放登录跳板机用户的公钥，内容格式同RSA公钥。
2. 运行脚本create_jumpserver.sh来创建docker镜像和对应的机器。
3. 登录跳板机
    `
    ssh -A -t -p 9022 root@bastion.address
    `
4.更改跳板机配置，以便维护。
  见各个文件夹下的README.md


## 更多信息：

敬请参考：

http://www.funtoo.org/Welcome

https://github.com/chentmin/bastion
