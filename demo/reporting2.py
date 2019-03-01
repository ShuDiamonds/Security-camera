#!/usr/bin/env python3
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

import json
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

import seaborn as sns
sns.set()

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

def ReportOnGmail(filesize1,filesize2,programstatus,yesturday):
	rawfiletmp = open("account.json" , "r")
	accountjsonfile = json.load(rawfiletmp)
	### add
	gmail_sender = accountjsonfile["username"] # Gmailのアドレス
	gmail_passwd = accountjsonfile["password"] # Gmailのパスワード

	SUBJECT = 'bulletin_'+date.today().strftime("%Y_%m_%d")# 件名
	TO = accountjsonfile["to_email"] # 送りたい先のアドレス
	FROM = gmail_sender

	outer = MIMEMultipart()
	outer['Subject'] = SUBJECT
	outer['To'] = TO
	outer['From'] = FROM
	outer.preamble = 'You will not see this in a MIME-aware mail reader.\n'
	mailbody="The olddest folder are deleted and {0}MB are relesed\n Security camera program is now active:{2}\n Yesterday file size was {1}MB".format(filesize1,filesize2,programstatus)
	part1 = MIMEText(mailbody, 'plain')
	outer.attach(part1)

	# Add attachments.
	attachments = ['./{0}/graph.png'.format(yesturday)]

	# attachments to base64 data. 
	for file in attachments:
		try:
			with open(file, 'rb') as fp:
			  msg = MIMEBase('application', "octet-stream")          
			  msg.set_payload(fp.read())
			encoders.encode_base64(msg)      
			msg.add_header('Content-Disposition', 'attachment', filename=os.path.basename(file))
			outer.attach(msg)
		except:
			print("Unable to open one of the attachments. Error: ", sys.exc_info()[0])           
			raise

	composed = outer.as_string()

	try:
		with smtplib.SMTP('smtp.gmail.com', 587) as s:
			s.ehlo()
			s.starttls()
			s.login(gmail_sender, gmail_passwd)
			s.sendmail(gmail_sender, TO, composed)
			s.close()
		print("Email sent!")
	except:
		print ('error sending mail')
		raise

	### end add
	
	return

def makegraph(yesturday):
	DATE_FORMAT = "%Y_%m_%d %H:%M:%S"
	my_date_parser = lambda d: pd.datetime.strptime(d, DATE_FORMAT)
	df = pd.read_csv('./{0}/data.csv'.format(yesturday), index_col=0, date_parser=my_date_parser, names=["time","x","y"])
	#print(df)
	df["count"]=1


	df2 = df["count"].resample('60min',how='sum')
	plt.figure()
	df2.plot()
	plt.savefig('./{0}/graph.png'.format(yesturday))
	plt.close('all')
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

def main():
	currentday=date.today().strftime("%Y_%m_%d")
	while(1):
		print(datetime.now().strftime("%Y_%m_%d")+str(check_program()))
		#debug
		with open("debug.txt", "a") as f:
			f.write(datetime.now().strftime("%Y_%m_%d")+str(check_program())+"\n")
		sleep(3600)
		
		if currentday != date.today().strftime("%Y_%m_%d"):#check the day is passed?
			#one day passed
			currentday = date.today().strftime("%Y_%m_%d")
			delfilesize=deleteoldestcameradata()
			
			tmppp=(date.today()- timedelta(1)).strftime("%Y_%m_%d")
			yesturdayfilesize=int(get_dir_size_old(tmppp)/1024/1024)
			makegraph(tmppp)
			ReportOnGmail(delfilesize,yesturdayfilesize,check_program(),tmppp)
		
if __name__ == '__main__':
	main()




