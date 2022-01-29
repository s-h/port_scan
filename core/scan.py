#!/usr/bin/env python3
from scanLog import scanLog
import re
import subprocess
import json

data = {}
# 单个ip，多个端口
def scan(ip, port_range):
    # scan("127.0.0.1", "1-10")
    cmd = "/usr/bin/nmap -T5 -sT -Pn -p "
    # cmd = "/usr/bin/nmap -sT -p "
    nmap_cmd = cmd + port_range + " " + ip
    status, res = subprocess.getstatusoutput(nmap_cmd)
    if status != 0:
        #print("nmap error")
        data["ip"] = ip
        data["port_status"] = "nmap error"
        #return (-1, "namp error") 
    #port_status = re.findall(r'(\d+)\/\S+\s+(open\|filtered|closed\|filtered|open|closed|filtered)',res)
    # 只返回open 及 open|filtered
    port_status = re.findall(r'(\d+)\/\S+\s+(open\|filtered|open)' ,res)
    data["ip"] = ip
    data["port_status"] = port_status
    return  json.dumps(data, ensure_ascii=False)


if __name__ == '__main__':
    print(scan("127.0.0.1", "1-65535"))
