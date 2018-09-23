from email import message
import smtplib
import json


rawfiletmp = open("./../demo/account.json" , "r")
accountjsonfile = json.load(rawfiletmp)
smtp_host = 'smtp.gmail.com'
smtp_port = 587
from_email = accountjsonfile["from_email"] # 送信元のアドレス
to_email = accountjsonfile["to_email"] # 送りたい先のアドレス
username = accountjsonfile["username"] # Gmailのアドレス
password = accountjsonfile["password"] # Gmailのパスワード
# メールの内容を作成
msg = message.EmailMessage()
msg.set_content('test mail') # メールの本文
msg['Subject'] = 'test mail(sub)' # 件名
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
