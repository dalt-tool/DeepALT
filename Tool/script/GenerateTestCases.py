#/usr/bin/python
#coding=utf-8

import os
import signal
import subprocess
import sys
import time
import datetime

class TestGenerator:

	def __init__(self, daltJar, appDir, testGenDir, outputDir, maxPathNum, sdkVersion):
		self.daltJar = daltJar
		self.appDir = appDir
		self.testGenDir = testGenDir
		self.outputDir = outputDir
		self.maxPathNum = maxPathNum
		self.sdkVersion = sdkVersion

	def runCommand(self, cmd_string, timeout):
		print("command is: " + cmd_string)
		p = subprocess.Popen(cmd_string, stderr=subprocess.STDOUT, stdout=subprocess.PIPE, shell=True, close_fds=True, preexec_fn=os.setsid)
		try:
			(msg,errs) = p.communicate(timeout=timeout)
			ret_code = p.poll()
			if ret_code:
				code = 1
				msg = "[Error]Called Error: " + str(msg.decode('utf-8'))
			else:
				code = 0
				msg = str(msg.decode('utf-8'))
		except subprocess.TimeoutExpired:
			p.kill()
			p.terminate()
			os.killpg(p.pid, signal.SIGTERM)
			code = 1
			msg = '[Error] Timeout Error: command ' + cmd_string + "timed out after " + str(timeout) + " seconds"
		return  code, msg

	def getSet(self,fn, aset):
		if not os.path.exists(fn):		
			f = open(fn, "w")
			f.close()
			
		#get apks
		f = open(fn, "r")
		lines = f.readlines()
		f.close()
		
		#add into set
		for x in lines:
			aset.add(x.strip())	
	
	def generateTC(self):
		if not os.path.exists(self.testGenDir):
			os.makedirs(self.testGenDir)
		if not os.path.exists(self.outputDir):
			os.makedirs(self.outputDir)
		print(self.appDir)

		fn = self.testGenDir +"history.txt"
		history_set = set()	
		self.getSet(fn,history_set)

		error_file = self.testGenDir + 'error_history.txt'
		
		#for each app
		apks = os.listdir(self.appDir)
		for apk in apks :
			if '.apk' in apk and '_ins.apk' not in apk:
				if apk in history_set:
					print(apk, "has been analyzed. To analyze again, modify " + fn)
					continue
				
				nowTime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
				print(nowTime)
				command = 'java -jar '+self.daltJar +' -v '+ str(self.sdkVersion) +' -p '+self.appDir+ ' -n ' +apk + " -maxPathNumber "  + str(self.maxPathNum) + ' -outputBasePath '+  self.testGenDir +'androlicOutput ' +' -o ' +self.testGenDir +' -exlib >  ' +  self.outputDir + apk[0:-4] + ".txt 2>&1"
				print(command + "\n")
				code, message = self.runCommand(command, 900)
				# os.system(command)
				f = open(fn, "a")
				f.write(apk + "\n")
				f.close()
				ef = open(error_file, 'a')
				if code == 1:
					ef.write(apk+"    " + message + "\n")
					print(apk+"    " + message)
				else:
					print("write apk ", apk)

				
				
if __name__ == '__main__' :
	daltJar = sys.argv[1]
	apk_input_dir = sys.argv[2] + os.sep
	testcase_dir = sys.argv[3]+ os.sep
	execute_info_dir = testcase_dir +sys.argv[4]+ os.sep
	max_number_of_path = sys.argv[5]
	
	generator = TestGenerator(daltJar, apk_input_dir, testcase_dir, execute_info_dir, max_number_of_path, 23)
	generator.generateTC()

	
