#!/bin/bash

target=$1
corr=$2
checker=$3
gen=$4

for ((i = 0; i < 100; i++))
do
	tst=`$gen`
	a=`echo $tst | $target`
	b=`echo $tst | $corr`
	if [ `$checker "$a" "$b" "$tst"` != "OK" ] 
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
