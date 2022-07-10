# -*- coding: utf-8 -*-
import subprocess
import time
import os,sys

class TimeoutError(Exception):
	pass
def executeCmd(cmd, timeout = 60):
	#pass
	s = subprocess.Popen(cmd, shell = True)
	print("execute ", cmd + "\n")
	beginTime = time.time()
	secondsPass = 0
	
	while True:
		if s.poll() is not None:
			break
		secondsPass = time.time() - beginTime
		if timeout and timeout < secondsPass:
			s.terminate()
			#print (str(timeout) +"s time out!")
			return False
	
		time.sleep(0.1)
	return True	





