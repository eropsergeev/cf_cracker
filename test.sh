#!/bin/bash

g++ -o prg "$1.cpp" -std=c++17 -Ofast -DONLINE_JUDGE || exit

for ((i = 0; i < 100; i++))
do
	tst=`./gen`
	#t1=`python3 -c "import time;print(int(time.time()))"`
	a=`echo $tst | ./prg | python3 check.py`
	b=`echo $tst | ./main | python3 check.py`
	#t2=`python3 -c "import time;print(int(time.time()))"`
	#let 't2 -= t1'
	if [ "$a" != "$b" ] 
	then
		echo "<a href=http://codeforces.com/contest/$2/challenge/$1>$1</a><br>" >> res.html
		tst=`echo "$tst" | python3 format.py`
		echo "$tst" >> res.html
		echo "<br>" >> res.html
		echo "$a<br>" >> res.html
		echo "$b<br>" >> res.html
		exit
	fi
done
