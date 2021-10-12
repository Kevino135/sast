#!/usr/bin/env python3

import os
import json
import argparse
from datetime import datetime

parser = argparse.ArgumentParser(description='Create report json ...')
parser.add_argument('--out', dest='names', required=True, help='report file name')
args = parser.parse_args()

get_name = args.names
to_time = datetime.strptime(str(get_name), "%d-%m-%Y %H:%M:%S")
fileName = to_time.strftime("%d-%m-%Y_%H:%M:%S")

dirs = 'logs/'
files = os.listdir(dirs)

result = []
for log_file in files:
    paths = dirs + log_file
    open_file = open(paths, 'r')
    content = open_file.readlines()
    open_file.close()

    report = {}
    report["scanner"] = log_file.replace('.json', '')
    report["report"] = []
    for log in content:
        data = json.loads(log) 
        (report["report"]).append(data)
    
    result.append(report)

print(json.dumps(result))

write_file = open(fileName + '.json', 'w')
write_file.write(json.dumps(result))
write_file.close()
