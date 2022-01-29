#!/usr/bin/env python3
from scan import scan
from sendMail import sendmail
from scanLog import scanLog
import json, time
import threading, queue
# 对比两次扫描端口状态，只关心新增开放端口
# 多线程使用nmap进行扫描

# ip配置文件
ip_config = "../config/ip.json"
# 结果保存文件
data_file = "../data/scan_res.json"
# 扫描结果
current = {}
# 对比结果
results = {}
# 主机扫描间隔(秒)
host_time = 0 
# 扫描并发
threads_count = 1
# 扫描端口范围
port_range = "1-65535"
# 定义日志文件
scanLog = scanLog(filename="../log/scan.log", default_level="info")

# 读取配置文件
with open(ip_config,'r',encoding='utf8')as fp:
    json_data = json.load(fp)

# 读取数据文件
with open(data_file, 'r', encoding='utf8') as fp:
    history_data = json.load(fp)

def write_data(data):
    data_json = json.dumps(data)
    with open(data_file, 'w') as fp:
        fp.write(data_json)

def checkPort(target_ip):
    scanLog.info("开始扫描ip：" + target_ip)
    target_describe = json_data[target_ip]
    target_scan = scan(ip=target_ip, port_range=port_range)
    target_scan = json.loads(target_scan)
    target_range_status = target_scan["port_status"]
    current[target_ip] = {}
    current[target_ip]["describe"] = target_describe
    current[target_ip]["port_status"] = target_range_status
    scanLog.info("%s describe ：%s" % (target_ip, target_describe))
    scanLog.info("%s port_status ：%s" % (target_ip, target_range_status))
    if target_range_status == "nmap error":
        scanLog.info("%s namp error" % target_ip)
    # 如果扫描ip不存在历史扫描中，results记录该ip所有端口状态
    if target_ip not in history_data:
        scanLog.info("上次扫描结果中未包含" + target_ip)
        results[target_ip] = {"describe": target_describe, "port_status": target_range_status}
        return True
    for port_status in target_range_status:
        if port_status not in history_data[target_ip]["port_status"]:
            scanLog.info("上次结果中不包含%s的端口%s")
            # target_ip不在results时记录
            if target_ip not in results:
                results[target_ip] = {}
                results[target_ip]["describe"] = target_describe
                results[target_ip]["port_status"] = [port_status]
            else:
                results[target_ip]["port_status"].append(port_status)
    # 每台主机扫描间隔
    time.sleep(host_time)
 

class test(threading.Thread):
    def __init__(self,q):
        threading.Thread.__init__(self)
        self._queue =q
 
    def run(self):
        while not self._queue.empty():
            ip=self._queue.get()
            checkPort(ip)

def main():
    scanLog.info("开始扫描")
    threads=[]
    q=queue.Queue()
    for target_ip in json_data:
        q.put(target_ip)
    for i in range(threads_count):
        threads.append(test(q))
    for i in threads:
        i.start()
    for i in threads:
        i.join()

if __name__ == '__main__':
    main()
    print("resutls:")
    print(results)
    # 写入数据文件
    write_data(current)
    # 根据结果发送邮件
    if results:
        sendmail(results)
