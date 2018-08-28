# coding: utf-8
import subprocess



keyword = "process_watching.py"
#cmd = "ps ax | grep " + keyword + " | grep -v grep | wc -l"
cmd = "ps ax | grep " + keyword + " | grep -v grep "
try:
	# result should be proess count string
	result = subprocess.check_output(cmd, shell=True).decode("utf-8").strip()
	if result != "2":
		#body = keyword + " process count was " + result + "!!!!"
		body = keyword + " process  was " + result
		print(body)
except Exception as e:
	body = str(e.args)


