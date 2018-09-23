# coding: utf-8
"""
main function are
reporting on gmail
delete one week ago camera data
program activity check (every one hour)
"""

import subprocess
from time import sleep
import os
from datetime import date, datetime, timedelta
import shutil

from email import message
import smtplib
import json


def check_program():
	keyword = "demo2.py"
	#cmd = "ps ax | grep " + keyword + " | grep -v grep | wc -l"
	cmd = "ps ax | grep " + keyword + " | grep -v grep "
	try:
		# result should be proess count string
		result = subprocess.check_output(cmd, shell=True).decode("utf-8").strip()
		if result != "2":
			#body = keyword + " process count was " + result + "!!!!"
			body = keyword + " process  was " + result
			#print(body)
			return True
	except Exception as e:
		body = str(e.args)
		#print("process was not found")
		return False
		
def get_dir_size_old(path='.'):
	total = 0
	for p in os.listdir(path):
	    full_path = os.path.join(path, p)
	    if os.path.isfile(full_path):
	        total += os.path.getsize(full_path)
	    elif os.path.isdir(full_path):
	        total += get_dir_size_old(full_path)
	return total

def ReportOnGmail(filesize1,filesize2,programstatus):
	rawfiletmp = open("account.json" , "r")
	accountjsonfile = json.load(rawfiletmp)
	smtp_host = 'smtp.gmail.com'
	smtp_port = 587
	from_email = accountjsonfile["from_email"] # 送信元のアドレス
	to_email = accountjsonfile["to_email"] # 送りたい先のアドレス
	username = accountjsonfile["username"] # Gmailのアドレス
	password = accountjsonfile["password"] # Gmailのパスワード
	# メールの内容を作成
	msg = message.EmailMessage()
	mailbody="The olddest folder are deleted and {0}MB are relesed\n Security camera program is now active:{2}\n Yesterday file size was {1}MB".format(filesize1,filesize2,programstatus)
	msg.set_content(mailbody) # メールの本文
	msg['Subject'] = 'bulletin_'+date.today().strftime("%Y_%m_%d")# 件名
	msg['From'] = from_email # メール送信元
	msg['To'] = to_email #メール送信先
	# メールサーバーへアクセス
	server = smtplib.SMTP(smtp_host, smtp_port)
	server.ehlo()
	server.starttls()
	server.ehlo()
	server.login(username, password)
	server.send_message(msg)
	server.quit()
	return

def deleteoldestcameradata():
	deletefilesize=0
	try:
		today = date.today()
		# 3日前
		seven_days_ago = (today - timedelta(7)).strftime("%Y_%m_%d")
		deletefilesize=int(get_dir_size_old(seven_days_ago)/1024/1024)
		shutil.rmtree(seven_days_ago)
	except Exception as e:
		body = str(e.args)
	print(body)
	return deletefilesize

if __name__ == '__main__':
	currentday=date.today().strftime("%Y_%m_%d")
	while(1):
		sleep(3600)
		print(datetime.now().strftime("%Y_%m_%d")+str(check_program()))
		if currentday != date.today().strftime("%Y_%m_%d"):#check the day is passed?
			#one day passed
			currentday = date.today().strftime("%Y_%m_%d")
			delfilesize=deleteoldestcameradata()
			
			tmppp=(date.today()- timedelta(1)).strftime("%Y_%m_%d")
			yesturdayfilesize=int(get_dir_size_old(tmppp)/1024/1024)
			
			ReportOnGmail(delfilesize,yesturdayfilesize,check_program())
		





