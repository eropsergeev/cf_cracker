#!/bin/bash

g++ -o prg "$1.cpp" -std=c++17 -Ofast -DONLINE_JUDGE || exit

for ((i = 0; i < 100; i++))
do
	tst=`./gen`
	a=`echo $tst | ./prg | python3 check.py`
	b=`echo $tst | ./main | python3 check.py`
	if [ "$a" != "$b" ] 
	then
		echo "<a href=http://codeforces.com/contest/$2/challenge/$1>$1</a><br>" >> res.html
		tst=`echo "$tst" | python3 -c "from sys import stdin, stdout;stdout.write(stdin.read().replace('\n', '<br>'))"`
		echo "$tst" >> res.html
		echo "<br>" >> res.html
		echo "$a<br>" >> res.html
		echo "$b<br>" >> res.html
		exit
	fi
done
