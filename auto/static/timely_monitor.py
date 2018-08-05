#!/usr/bin/python3

# apt install -y python3-pip && pip3 install psutil
import json, psutil, time

res = {}

res['cpu_percent'] = psutil.cpu_percent(1)
res['memory_percent'] = psutil.virtual_memory().percent
res['disk_percent'] = psutil.disk_usage('/').percent

print(json.dumps(res))

