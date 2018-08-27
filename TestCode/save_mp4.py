# -*- Coding: utf-8 -*-
import cv2
from datetime import datetime
import numpy as np


height=240
width=320
# カメラのキャプチャを開始 --- (*1)
cam = cv2.VideoCapture(0)

cam.set(cv2.CAP_PROP_FPS, 10)           # カメラFPSを60FPSに設定
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, height) # カメラ画像の縦幅を240に設定
cam.set(cv2.CAP_PROP_FRAME_WIDTH, width) # カメラ画像の横幅を320に設定

print(cam.get(cv2.CAP_PROP_FPS))
print(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
print(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))

#フォントの大きさ
fontscale = 0.3
#フォントカラー(B, G, R)
color=(255, 255, 255)
#フォント
fontface = cv2.FONT_HERSHEY_SIMPLEX

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('./output.avi',fourcc, 20.0, (640,480))

while True:
	# 画像を取得 --- (*2)
	_, img = cam.read()
	cv2.putText(img,datetime.now().strftime("%Y/%m/%d %H:%M:%S"),(width-120,height-5),fontface,fontscale, color)
	# write the flipped frame
	out.write(img)
	# ウィンドウに画像を表示 --- (*3)
	cv2.imshow('PUSH ESC KEY', img)
	# escキーが押されたら終了する
	if cv2.waitKey(1) == 0x1b: break
# 後始末
cam.release()
out.release()
cv2.destroyAllWindows()
