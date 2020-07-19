import sys
import subprocess
import os
from decouple import config

IP_NETWORK = config('IP_NETWORK')
IP_SEBASTIAN = config('IP_SEBASTIAN')

proc = subprocess.Popen(["ping", IP_NETWORK], stdout=subprocess.PIPE)
while True:
    line = proc.stdout.readline()
    if not line:
        break
    # the real code does filtering here
    connected_ip = line.decode('utf-8').split()[3]
    print(connected_ip)
    if(connected_ip == IP_SEBASTIAN):
        print("Connected")
        subprocess.Popen(["say", "Sebastian just connected to the network"])
        break
