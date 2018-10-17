# smtplib module send mail
import sys
import os
import json
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

rawfiletmp = open("./../demo/account.json" , "r")
accountjsonfile = json.load(rawfiletmp)
# Gmail Sign In
gmail_sender = accountjsonfile["username"] # Gmailのアドレス
gmail_passwd = accountjsonfile["password"] # Gmailのパスワード

SUBJECT = 'TEST'
TO = accountjsonfile["to_email"] # 送りたい先のアドレス
FROM = gmail_sender

outer = MIMEMultipart()
outer['Subject'] = SUBJECT
outer['To'] = TO
outer['From'] = FROM
outer.preamble = 'You will not see this in a MIME-aware mail reader.\n'

part1 = MIMEText("マルセイバターサンド", 'plain')
outer.attach(part1)

# Add attachments.
attachments = ['./aaa.png']

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


