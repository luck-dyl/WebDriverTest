配置新网站
=======================
## 创建普通账号，但是用超级管理权限
1、用root帐号登录或者su到root。添加新用户：sudo useradd xiaohon(账号名称)
2、增加sudoers文件的写权限： chmod u+w /etc/sudoers
3、vim /etc/sudoers 找到 root ALL=(ALL) ALL 在这行下边添加 xiaohon ALL=(ALL) ALL  (ps:xiaohon代表是你要添加sudo权限的用户名)
4、除去sudoers文件的写权限： chmod u-w /etc/sudoers
5、设置账号密码：“ passwd xiaohon(用户名)” 输入密码，确认一次，root用户密码也可以这样修改
？我设置了密码， 可以使用su root 切换过去， 但是普通用户执行 sudo命令密码就错误了？？？

## 需要的包：
* nginx
* Python 3.6
* virtualenv + pip
* Git
以Ubuntu为例：
sudo apt-get update
sudo apt-get install python-software-properties
sudo apt-get install software-properties-common
sudo add-apt-repository ppa:fkrull/deadsnakes
sudo apt-get update
sudo apt-get install nginx git python3.6 python3.6-venv
[** 注意当你copy这些命令时，可能在服务中执行失败，可以手动输入，或检查命令是否有多余的空格]
## Nginx虚拟主机
* 参考nginx.template.conf
* 把SITENAME替换成所需的域名，例如staging.my-domain.com
创建软连接：（请使用完整目录，我之前没有，导致失败）
* sudo ln -s /etc/nginx/sites-available/superlists-test.ddns.net /etc/nginx/sites-enabled/superlists-test.ddns.net
sudo systemctl reload nginx
../virtualenv/bin/python manage.py runserver
访问服务器IP,查看网站是否运行正常
## Systemd服务
* 参考gunicorn-upstart.template.conf
* 把SITENAME替换成所需的域名，例如staging.my-domain.com
* 把“pls pull your real emailpassword”替换成电子邮件密码
## 文件夹结构：
假设有用户账户，家目录为/home/username
/home/username
└─ sites
 └─ SITENAME
 ├─ database
 ├─ source
 ├─ static
 └─ virtualenv