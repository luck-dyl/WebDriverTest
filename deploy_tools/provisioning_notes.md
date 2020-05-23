配置新网站
=======================
## 配置普通账号，授权根目录，和sudo命令
1、用root帐号登录或者su到root。添加新用户：xiaohon(账号名称)
sudo adduser xiaohon

2、增加sudoers文件的写权限： 
chmod u+w /etc/sudoers

3、vim /etc/sudoers 找到 root ALL=(ALL) ALL 在这行下边添加
xiaohon ALL=(ALL) ALL  
(ps:xiaohon代表是你要添加sudo权限的用户名，其实不一定要找到对应的”root 下”，只需在底部加上这一句也可以)

4、除去sudoers文件的写权限： chmod u-w /etc/sudoers

5、切换到普通用户
su xiaohon

6、执行sudo命令时，输入的密码是当前普通用户的登录密码

## 需要的包：
* nginx
* Python 3.6
* virtualenv + pip
* Git
以Ubuntu为例：
 sudo add-apt-repository ppa:fkrull/deadsnakes
 sudo apt-get install nginx git python36 python3.6-venv
 
## Nginx虚拟主机
* server: /etc/nginx/sites-available/superlists-staging.ottg.eu（随便命名）
* 参考nginx.template.conf
* 把SITENAME替换成所需的域名，例如staging.my-domain.com
* 然后创建一个符号链接，把这个文件加入启用的网站列表中：
elspeth@server:$ sudo ln -s ../sites-available/superlists-staging.ottg.eu /etc/nginx/sites-enabled/superlists-staging.ottg.eu
elspeth@server:$ ls -l /etc/nginx/sites-enabled # 确认符号链接是否在那里
elspeth@server:sudo systemctl reload nginx

## Systemd服务
* server: /etc/systemd/system/gunicorn-superlists-staging.ottg.eu.service
* 参考gunicorn-upstart.template.conf
* 把SITENAME替换成所需的域名，例如staging.my-domain.com
* 把“pls pull your real emailpassword”替换成电子邮件密码

* 必须执行这个命令，让Systemd加载新的配置文件
elspeth@server:$ sudo systemctl daemon-reload
* 这个命令让Systemd在引导时加载服务
elspeth@server:$ sudo systemctl enable gunicorn-superlists-staging.ottg.eu
* 这个命令启动服务
elspeth@server:$ sudo systemctl start gunicorn-superlists-staging.ottg.eu

## 文件夹结构：
假设有用户账户，家目录为/home/username
/home/username
└─ sites
 └─ SITENAME
 ├─ database
 ├─ source
 ├─ static
 └─ virtualenv