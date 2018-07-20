#!/usr/bin/python3
from urllib.request import *
from sys import *
import re
from tqdm import tqdm
from queue import Queue
import os
from threading import *
from time import sleep

problem = ''
contest_number = argv[1] if len(argv) > 1 else '1006'

lang_set = {'cpp', 'pas', 'php', 'js'}

def get_code(n):
	try:
		with urlopen("http://codeforces.com/contest/" + contest_number + "/submission/" + str(n), timeout = 1) as f:
			s = f.read().decode()
	except:
		return None
	if (s.count(str(contest_number)) == 0 or s.count("<span class='verdict-accepted'>Accepted</span>") == 0):
		return None
	lang_pos = s.split('<pre id="program-source-text"')[1][:100].find('lang-') + 5
	if (lang_pos < 5):
		lang = 'pas'
	else:
		lang = s.split('<pre id="program-source-text"')[1][lang_pos:lang_pos+10].split()[0]
	if lang not in lang_set:
		return None
	s = s.split('<pre id="program-source-text"')[1].split(">")[1]
	s = s.split("</pre")[0]
	s = s.replace("&lt;", '<')
	s = s.replace("&gt;", '>')
	s = s.replace("&quot;", '"')
	s = s.replace("&amp;", '&')
	p = s.find("&#")
	while (p != -1):
		s = s[:p] + chr(int(s[p + 2: p + 4])) + s[p + 5:]
		p = s.find("&#")
	return s, lang

def get_list(n):
	with urlopen("http://codeforces.com/contest/" + str(contest_number) + "/status/page/" + str(n) + "?order=BY_ARRIVED_DESC") as f:
		s = f.read().decode()
	preans = list(set(re.findall(r'[0-9]{8}', s)))
	ans = []
	for x in preans:
		p = s.find(x)
		if (s[p:p + 1000].count('submissionVerdict="OK"') != 0 and s[p:p + 1000].count('/contest/' + contest_number + '/problem/') != 0):
			ind = s[p:p + 1000].find('/contest/' + contest_number + '/problem/') + len('/contest/' + contest_number + '/problem/')
			ans.append((x, s[p + ind]))
	return ans

def get_executable(code, lang, prefix = ''):
	with open('/tmp/' + prefix + 'code.' + lang, 'w') as f:
		f.write(code)
	if (lang == 'cpp'):
		os.system('g++ -std=c++17 -DONLINE_JUDGE -o /tmp/' + prefix + 'main /tmp/' + prefix + 'code.cpp > /dev/null')
		return '/tmp/' + prefix + 'main'
	elif (lang == 'pas'):
		os.system('fpc /tmp/' + prefix + 'code.pas > /dev/null')
		return '/tmp/' + prefix + 'code'
	else:
		return '"' + lang + ' /tmp/' + prefix + 'code.' + lang + '"'

def run():
	global runed
	while True:
		if not runed:
			return
		if not q.empty():
			code, lang, problem = q.get()
			target = get_executable(code, lang)
			os.system('./test.sh ' + target + ' ' + correct_solution + ' ' + checker + ' ' + test_gen + ' ' + problem + ' ' + contest_number)
			q.task_done()

def start():
	global runed
	if (runed):
		return
	runed = True
	main_thread.start()

def stop():
	global runed
	global main_thread
	if not runed:
		return
	runed = False
	main_thread.join()
	main_thread = Thread(target=run)

class MyQueue(Queue):
	def __init__(self):
		self.sz = 0
		super().__init__()
	def put(self, x):
		self.sz += 1
		super().put(x)
	def get(self):
		self.sz -= 1
		return super().get()
	def size(self):
		return self.sz;


if __name__ == "__main__":
	submitions_list = []
	q = MyQueue()
	runed = False
	main_thread = Thread(target=run)
	while (True):
		try:
			args = input().split()
		except:
			continue
		if not(len(args)):
			continue
		command = args[0]
		if (command[0] == '#'):
			continue
		args = args[1:]
		if (command == 'help'):
			print('contest <X> - set contest number')
			print('list <from> <to> - generate submitions list')
			print('clear <list|queue> - clear submissions list or queue')
			print('code <X> - get source codes for problem X and put it to queue')
			print('set <correct_solution|checker|test_gen> <value> - no coments')
			print('start - start testing')
			print('stop - stop testing')
			print('size - queue size')
			print('exit - exit')
			print('wait <n> - wait n seconds')
		elif (command == 'contest' and len(args) >= 1):
			contest_number = args[0]
		elif (command == 'list' and len(args) >= 2):
			for i in tqdm(range(int(args[0]), int(args[1]))):
				submitions_list += get_list(i)
		elif (command == 'clear' and len(args) >= 1):
			if (args[0] == 'list'):
				submitions_list = []
			elif (args[0] == 'queue'):
				stop()
				q = Queue()
		elif (command == 'stop'):
			stop()
		elif (command == 'code' and len(args) >= 1):
			for (num, problem) in tqdm(submitions_list):
				if (problem == args[0]):
					code = get_code(num)
					if (code):
						q.put(code + (num,))
		elif (command == 'start'):
			start()
		elif (command== 'size'):
			print(q.size())
		elif (command == 'set'):
			if (args[0] == 'correct_solution'):
				try:
					correct_solution = get_executable(*get_code(args[1]), 'corr_')
				except:
					print("error!")
			elif (args[0] == 'checker'):
				checker = ' '.join(args[1:])
			elif (args[0] == 'test_gen'):
				test_gen = ' '.join(args[1:])
		elif (command == 'exit'):
			stop()
			exit()
		elif (command == 'wait' and len(args) >= 1):
			sleep(int(args[0]))
		else:
			print("command not found")
