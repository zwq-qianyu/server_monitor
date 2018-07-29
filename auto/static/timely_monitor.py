#!/usr/bin/python3

# apt install -y python3-pip && pip3 install psutil
import json, psutil, time

res = {}

i = 0
while i<10:
	with open("monitor.txt",'a') as f:
		res['cpu_percent'] = psutil.cpu_percent(1)
		res['memory_percent'] = psutil.virtual_memory().percent
		res['disk_percent'] = psutil.disk_usage('/').percent
		f.write(json.dumps(res)+"\n")
		f.close()
		print(json.dumps(res))
		i += 1
		time.sleep(1)

