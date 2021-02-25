#! usr/bin/env python

import sys
import socket
import threading
import argparse
from queue import Queue
from datetime import datetime

print('''
	 ____      ___   ___    __    _  _ 
	(  _ \    / __) / __)  /__\  ( \( )
	 )___/___ \__ \( (__  /(__)\  )  ( 
	(__) (___)(___/ \___)(__)(__)(_)\_)
			by : Abdul_Samad''')

socket.setdefaulttimeout(0.75)
print_lock = threading.Lock()

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", dest="target", help="Target-Ip / Host_Name")
    parser.add_argument("-p", "--ports", dest="port", help="Enter the last # of port <eg: 1000>")
    options = parser.parse_args()
    if not options.target:
        parser.error("[-] Please specify the Target Ip / Host Name")
    elif not options.port:
        parser.error("[-] Please specify the last port in the range e.g: 1000")
    return options
options = get_args()
target = socket.gethostbyname(options.target)
print("-"*50 + "\n"  +"Scaning target : " + target + "\n" + "Time started at : " + str(datetime.now()) + "\n" + "-"*50)

def scan(port):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		result = s.connect((target,port))
		with print_lock:
			print(str(port) + " is open")
		s.close()
	except:
		pass

def threader():
    while True:
        ports = q.get()
        scan(ports)
        q.task_done()

q = Queue()

for x in range(100):
    t = threading.Thread(target=threader)
    t.daemon = True
    t.start()

for ports in range(1, int(options.port)):
    q.put(ports)

q.join()
