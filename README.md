A email client in terminal

Introduction

emcli is inspired by mutt, enable you send email in terminal handy.

Installation

To install emcli, simply:

pip install emcli
Or install emcli from source code:

git clone https://github.com/gucci/emcli
cd emcli
sudo python setup.py install
Usage

save emcli settings in ~/.emcli.cnf:

$ cat ~/.emcli.cnf
[DEFAULT]
smtp_server = smtp.qq.com
smtp_port = 25
username = x403720692@qq.com
password = abc123

send email to multiple recipents and attache:

python emcli.py -s TEST -b "/etc/password" -a logger.py,storage.py -r xx@xx.com,xx2@xx.com

send email with stdin:

python emcli.py -s TEST -b "/etc/password" -a logger.py,storage.py -r xx@xx.com,xx2@xx.com < /etc/password
