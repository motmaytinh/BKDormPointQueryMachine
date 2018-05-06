"""Auto get student's point in BK Dormitory"""
import requests
import re
import time
import threading
import Queue

URL = "http://ktxbk.vn/index.php?option=com_svdkonline&view=hdtd"
NUM_THREAD_WORKER = 25

def get_mssv():
	f = open('ktx.txt','r')
	s = f.read()
	f.close()
	file = open("list.txt", 'w')

	data = re.findall(r'<td>[K0-9]+</td>',s)
	for one in data:
		sv = re.sub(r'<td>|</td>',"",one)
		file.write(sv+'\n')
	file.close()

def get_point():
	session = requests.Session()
	while True:
		mssv = queue.get()
		RESPONSE = session.post(URL, data={'loaithe':'SV', 'tu_khoa':str(mssv), 'hk':'2', 'th':'1', 'nh':'2017', 'option':'com_svdkonline'}, stream=True)
		RESPONSE.raise_for_status()
		s = RESPONSE.text
		data = re.search(r'[0-9]*</b></font><br />',s,re.I)
		if data:
			point = re.sub(r'</b></font><br />',"",data.group())
			with lock:
				f.write(mssv + ',' + point + '\n')
		# else: 
		# 	with lock:
		# 		f.write(mssv + ',' + '0' + '\n')
		queue.task_done()				

f = open("point.txt", 'w')
lock = threading.Lock()
queue = Queue.Queue()
start = time.time()
def main():
	get_mssv()
	
	downloadThreads = []

	for i in range(NUM_THREAD_WORKER):
		# downloadThread = threading.Thread(target=get_point, args=(queue,))
		downloadThread = threading.Thread(target=get_point)
		downloadThread.setDaemon(True)
		downloadThread.start()
		downloadThreads.append(downloadThread)

	p = open("list.txt", "r")
	for line in p:
		queue.put(line.strip('\n'))
	queue.join()

	print "Elapsed Time: %s" % (time.time() - start)
		
if __name__== "__main__":
	main()
