# -*- Coding: utf-8 -*-
import cv2
from datetime import datetime
from scipy import ndimage

height=240
width=320
# カメラのキャプチャを開始 --- (*1)
cam = cv2.VideoCapture(0)
cam2 = cv2.VideoCapture(1)

cam.set(cv2.CAP_PROP_FPS, 10)           # カメラFPSを60FPSに設定
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, height) # カメラ画像の縦幅を240に設定
cam.set(cv2.CAP_PROP_FRAME_WIDTH, width) # カメラ画像の横幅を320に設定

cam2.set(cv2.CAP_PROP_FPS, 10)           # カメラFPSを60FPSに設定
cam2.set(cv2.CAP_PROP_FRAME_HEIGHT, height) # カメラ画像の縦幅を240に設定
cam2.set(cv2.CAP_PROP_FRAME_WIDTH, width) # カメラ画像の横幅を320に設定

print(cam.get(cv2.CAP_PROP_FPS))
print(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
print(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))

#フォントの大きさ
fontscale = 0.3
#フォントカラー(B, G, R)
color=(255, 255, 255)
#フォント
fontface = cv2.FONT_HERSHEY_SIMPLEX



while True:
	# 画像を取得 --- (*2)
	_, img = cam.read()
	_, img2 = cam2.read()
	img = ndimage.rotate(img, 180, reshape=False)

	cv2.putText(img,datetime.now().strftime("%Y/%m/%d %H:%M:%S"),(width-120,height-5),fontface,fontscale, color)
					
	cv2.putText(img2,datetime.now().strftime("%Y/%m/%d %H:%M:%S"),(width-120,height-5),fontface,fontscale, color)

	# ウィンドウに画像を表示 --- (*3)
	#cv2.imshow('PUSH ESC KEY', img)
	cv2.imshow('PUSH ESC KEY2', img)
	# escキーが押されたら終了する
	key = cv2.waitKey(1)
	if key == 0x1b: 
		cv2.imwrite("takepic.jpg", img)
		break

# 後始末
cam.release()
cam2.release()
cv2.destroyAllWindows()
