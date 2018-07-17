#!/usr/bin/env python

import sys
import shlex
import subprocess
import time
from datetime import datetime
from collections import OrderedDict

def meminfo():
	'''	return the info of /proc/meminfo
	as a dictionary
	'''
	meminfo = OrderedDict()
	with open('/proc/meminfo') as f:
		for line in f:
			meminfo[line.split(':')[0]] = line.split(':')[1].strip()
	return meminfo

def monitor(pid, fpath):
	with open(fpath, 'wb+') as fd:
		info = "TIME    VIRT RES SHR %MEM %CPU"
		fd.write(info + "\n")
		while True:
			cur_time = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
			cmd = "top -b -p %s -n 1 | grep %s" % (pid, pid)
			cmd_arr = shlex.split(cmd)
			proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
			stdout, stderr = proc.communicate()
			#print "stdout", stdout, "stderr", stderr
			pieces = stdout.strip().split(" ")
			while '' in pieces:
				pieces.remove('')
			if len(pieces) == 0:
				break
			info = "%s %s %s %s %s %s" % (cur_time, 
										pieces[4], 
										pieces[5], 
										pieces[6], 
										pieces[9],
										pieces[8])
			fd.write(info + "\n")
			print info
			time.sleep(1)

if __name__ == '__main__':
	monitor(sys.argv[1], sys.argv[2])
