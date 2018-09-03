# -*- Coding: utf-8 -*-
import cv2
from datetime import datetime
import numpy as np
from time import sleep
import csv

height=240
width=320
fps=2

#フォントの大きさ
fontscale = 0.35
#フォントカラー(B, G, R)
color=(0, 0, 255)
#フォント
fontface = cv2.FONT_HERSHEY_SIMPLEX

# 保存パスの指定
save_path = "./"
lifetime=10

# 画像に動きがあったか調べる関数
def check_image(img1, img2, img3):
    # グレイスケール画像に変換 --- (*6)
    gray1 = cv2.cvtColor(img1, cv2.COLOR_RGB2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_RGB2GRAY)
    gray3 = cv2.cvtColor(img3, cv2.COLOR_RGB2GRAY)
    # 絶対差分を調べる --- (*7)
    diff1 = cv2.absdiff(gray1, gray2)
    diff2 = cv2.absdiff(gray2, gray3)
    # 論理積を調べる --- (*8)
    diff_and = cv2.bitwise_and(diff1, diff2)
    # 白黒二値化 --- (*9)
    _, diff_wb = cv2.threshold(diff_and, 30, 255, cv2.THRESH_BINARY)
    # ノイズの除去 --- (*10)
    diff = cv2.medianBlur(diff_wb, 5)
    return diff

# moment
def cal_moment(img):
	mu = cv2.moments(img, False)
	x,y= int(mu["m10"]/mu["m00"]) , int(mu["m01"]/mu["m00"])
	
	with open('data.csv', 'a') as f:
		writer = csv.writer(f, lineterminator='\n') # 改行コード（\n）を指定しておく
		writer.writerow([datetime.now().strftime("%Y_%m_%d %H:%M:%S"),x,y])     # list（1次元配列）の場合
	
	return x,y

# カメラから画像を取得する
def get_image(cam):
    img = cam.read()[1]
    sleep(0.5)
    #img = cv2.resize(img, (600, 400))
    return img

if __name__ == '__main__':
    # カメラのキャプチャを開始 --- (*1)
	cam = cv2.VideoCapture(0)

	cam.set(cv2.CAP_PROP_FPS, 10)           # カメラFPSを60FPSに設定
	cam.set(cv2.CAP_PROP_FRAME_HEIGHT, height) # カメラ画像の縦幅を240に設定
	cam.set(cv2.CAP_PROP_FRAME_WIDTH, width) # カメラ画像の横幅を320に設定

	# フレームの初期化 --- (*1)
	img1 = img2 = img3 = get_image(cam)
	th = 50
	
	# Define the codec and create VideoWriter object
	fourcc = cv2.VideoWriter_fourcc(*'XVID')
	
	
	while True:
		out = cv2.VideoWriter('./output_{0}.avi'.format(datetime.now().strftime("%Y_%m_%d %H:%M:%S")),fourcc, fps, (width,height))
		StartTime=datetime.now()
		
		while True:
			#check pass 1hour or not 
			if (datetime.now()-StartTime).total_seconds()>3600:
				break
			# ESCキーが押されたら終了
			if cv2.waitKey(1) == 0x1b: break
			# 差分を調べる --- (*2)
			diff = check_image(img1, img2, img3)
			# 差分がthの値以上なら動きがあったと判定 --- (*3)
			cnt = cv2.countNonZero(diff)
			x=0
			y=0
			if cnt > th:
				
				x,y=cal_moment(diff)
				print("カメラに動きを検出")
				lifetime=10
			else:
				print(str(lifetime)+":"+datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
				lifetime=lifetime-1 #5sec saved
				if lifetime<0:
					lifetime=0
				
			if lifetime>0:
				tmpimg=img3
			else:
				tmpimg=diff
			
			cv2.putText(tmpimg,datetime.now().strftime("%Y/%m/%d %H:%M:%S"),(width-130,height-5),fontface,fontscale, color)
			cv2.imshow('PUSH ESC KEY', tmpimg)
			
			# 写真を画像 --- (*4)
			#cv2.imwrite(save_path + str(num) + ".jpg", img3)
			out.write(tmpimg)
		
		
			# 比較用の画像を保存 --- (*5)
			img1, img2, img3 = (img2, img3, get_image(cam))
		
		#1hour while-loop
		out.release()
		# ESCキーが押されたら終了
		if cv2.waitKey(1) == 0x1b: break
	# 後始末
	cam.release()
	out.release()
	cv2.destroyAllWindows() 



