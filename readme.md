# port_scan
使用nmap多线程扫描端口，只关注新增端口，新增开放端口发送邮件。

## 配置
./config/ip.json 被扫描ip

./core/sendMail.py 配置发送与接收结果邮箱

## 执行
python3 ./core/main.py


