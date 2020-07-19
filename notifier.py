import os
import sys
import subprocess
import nmap                         # import nmap.py
import time
import re
from decouple import config

IP_NETWORK = config('IP_NETWORK')
IP_JULIAN = config('IP_JULIAN')
IP_SEBASTIAN = config('IP_SEBASTIAN')


sebPresent = False
sebPrev = True

try:
    nm = nmap.PortScanner()         # instance of nmap.PortScanner
except nmap.PortScannerError:
    print('Nmap not found', sys.exc_info()[0])
    sys.exit(0)
except:
    print("Unexpected error:", sys.exc_info()[0])
    sys.exit(0)

hostList = []
gracePeriod = 7

# Add people that stays in network
# Remove them when they leave so that the alert wont run forever


def seek():                         # function to scan the network
    curHosts = []
    nm.scan(hosts='192.168.1.0/24', arguments='-n -sP -PE -T5')
    # executes a ping scan

    localtime = time.asctime(time.localtime(time.time()))
    print('============ {0} ============'.format(localtime))
    # system time
    global sebPresent
    global sebPrev
    for host in nm.all_hosts():
        try:
            mac = nm[host]['addresses']['mac']
            vendor = nm[host]['vendor'][mac]
        except:
            vendor = mac = 'unknown'

        curHosts.append((host, mac, vendor, gracePeriod))

    updateHostList(curHosts)

    for host in hostList:
        if((host[0] == IP_SEBASTIAN) and not sebPresent):
            print("Sebastain connected with IP: {}".format(host[0]))
            alert("Sebastian")

    for host in hostList:
        if((host[0] == IP_SEBASTIAN)):
            sebPresent = True
            break

        sebPresent = False

    if (sebPrev) and (not sebPresent):
        justLeft("Sebastian")

    sebPrev = sebPresent
    return len(hostList)                # returns count


def initPresent():
    return False


def updateHostList(curHosts):
    global hostList
    if hostList == []:
        hostList = curHosts
    else:
        hostList = [(x[0], x[1], x[2], x[3]-1) for x in hostList]

        # only the hosts that were new in this iteration
        newList = [(x[0], x[1], x[2], x[3])
                   for x in curHosts if not (any(x[0] == y[0] for y in hostList))]

        for host in newList:
            hostList.append(host)

        for host in hostList:
            if any(host[0] == y[0] for y in curHosts):
                hostList[hostList.index(host)] = (
                    host[0], host[1], host[2], gracePeriod)

        for host in hostList:
            if host[3] <= 0:
                hostList.remove(host)


def alert(name):
    # Audio message when specific person connects to internet
    subprocess.Popen(["say", "{} just arrived".format(name)])


def justLeft(name):
    # Audio message when specific person disconnects from internet
    subprocess.Popen(["say", "{} just left".format(name)])


if __name__ == '__main__':
    old_count = new_count = seek()

    startCounter = gracePeriod
    # are there any new hosts?
    while True:
        startCounter -= 1
        time.sleep(1)               # increase to slow down the speed
        old_count = new_count
        new_count = seek()
