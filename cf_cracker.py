#!/usr/bin/python3
from urllib.request import *
from sys import *
import re
from tqdm import tqdm
from queue import Queue
import os
from threading import *

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
			ans.append(x, s[p + ind])
	return ans

def get_executable(code, lang, prefix = ''):
	with open('/tmp/code.' + lang, 'w') as f:
		f.write(code)
	if (lang == 'cpp'):
		os.system('g++ -std=c++17 -DONLINE_JUDGE -o /tmp/' + prefix + 'main /tmp/' + prefix + 'code.cpp 12> /dev/null')
		return '/tmp/' + prefix + 'main'
	elif (lang == 'pas'):
		os.system('fpc /tmp/' + prefix + 'code.pas 12> /dev/null')
		return '/tmp/' + prefix + 'code'
	else:
		return '"' + lang + ' /tmp/' + prefix + 'code.' + lang + '"'

def run():
	while True:
		if not runed:
			return
		if not q.empty():
			code, lang = q.get()
			target = get_executable(code, lang)
			os.system('./test.sh ' + target + ' ' + correct_solution + ' ' + checker + ' ' + test_gen)
			q.task_done()

def start(correct_solution_, checker_, test_gen_):
	if (runed):
		return
	global test_gen
	global correct_solution
	global checker
	checker = checker_
	correct_solution = get_executable(*get_code(correct_solution_), 'corr_')
	test_gen = test_gen_
	runed = True
	main_thread.start()

def stop():
	if not runed:
		return
	runed = False
	main_thread.join()


if __name__ == "__main__":
	submitions_list = []
	q = Queue()
	runed = False
	main_thread = Thread(target=run)
	while (True):
		args = input().split()
		command = args[0]
		args = args[1:]
		if (command == 'help'):
			print('contest <X> - set contest number')
			print('list <from> <to> - generate submitions list')
			print('clear <list|queue> - clear submissions list or queue')
			print('code <X> - get source codes for problem X and put it to queue')
			print('start <correct_solution> <checker> <test_gen> - start testing')
			print('stop - stop testing')
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
						q.put(code)
		elif (command == 'start'):
			start(*args)
		else:
			print("command not found")
