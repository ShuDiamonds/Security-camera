<div style="; position: relative;top:0; left: 100px;"></div>
<img src="https://github.com/ShuDiamonds/Security-camera/blob/master/image/python_illustration.svg" height="150" width="300">

# Security-camera
This python code is a security camera program using `USB Web Cam`. in this product. The system output the avi video which is captured with "difference extraction" technology.

## Main Features
* Strong Reduction of its SD memory occupation with `difference extraction` Technology.
* Reporting a daily bulletin through on Gmail.
* Supervise the [main program](https://github.com/ShuDiamonds/Security-camera/blob/master/demo/demo2.py) by [reporting.py](https://github.com/ShuDiamonds/Security-camera/blob/master/demo/reporting.py).

## System Overview
<p align="center"> 
<img  src="https://github.com/ShuDiamonds/Security-camera/blob/master/image/Securitycamera_SystemOverview.svg.png"  title="system overview">
</p>
  
## Requirement  
* Raspberry pi 3  
* ubuntu16.04  
* Python 3.x  
* Opencv
* Web Camera x2
 <p align="center"> 
<img  src="https://github.com/ShuDiamonds/Security-camera/blob/master/image/IMG_20180927_215417.jpg"  title="setting" width="480">
</p>
 
## Setting
###  demo2.py property
* image size
 adjust heght and width variables.

### reporting.py property
Set the email infomation to send a daily report through on gmail.
```
from_email = "senderhogehoge@gmail.com" # 送信元のアドレス
to_email = "receiverhogehoge@gmail.com" # 送りたい先のアドレス
username = "sender@gmail.com"           # Gmailのアドレス
password = "mygmailpassword"            # Gmailのパスワード
```
and you have to lower its Google Security level (if not doing that, you can't send email from gmail and recieve the security alart mail from google).

## Usage
### Basic Example
```bash
$ python3 demo2.py
```
### report program example
In this program, Raspberry pi read a variable register value(0-255) on `PCF8591` default setting. And 
output to LED(located at lowwer in this picture) which is on PCF8591 using Digital analog converter.
```bash
$ python3 reporting.py
```


## Licence

  [MIT](https://github.com/tcnksm/tool/blob/master/LICENCE)

## Related Articles
* [embedded](https://github.com/topics/shu-embedded-systems)
* [Machine Learning data](https://github.com/topics/shu-machine-learning-data)

## Author
  [ShuDiamonds](https://github.com/ShuDiamonds)
