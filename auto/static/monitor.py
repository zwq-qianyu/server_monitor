#!/usr/bin/python3

# apt install -y python3-pip && pip3 install psutil
import json, psutil

res = {}

res['cpu_count'] = psutil.cpu_count()
res['memory_total'] = int(psutil.virtual_memory().total / 1024 / 1024)
res['disk_total'] = int(psutil.disk_usage('/').total / 1024 / 1024 / 1024)

res['cpu_percent'] = psutil.cpu_percent(1)
res['memory_percent'] = psutil.virtual_memory().percent
res['disk_percent'] = psutil.disk_usage('/').percent

print(json.dumps(res))
