### sshserver使用

使用一台服务器（or docker服务器，centos最佳）

1.安装mysql server，导入db目录中的devops.sql

2.根据ljops_server/requirements.txt，安装依赖

（tips：python依赖包导出：pip freeze > requirements.txt）

### 注意：
本机器需要和其他服务器建立互信（root级别），后续会调用该机器去同其他服务器建立互信。
