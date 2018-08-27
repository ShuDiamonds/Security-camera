# -*- Coding: utf-8 -*-
import cv2
from datetime import datetime


height=240
width=320

#フォントの大きさ
fontscale = 0.3
#フォントカラー(B, G, R)
color=(255, 255, 255)
#フォント
fontface = cv2.FONT_HERSHEY_SIMPLEX

# 保存パスの指定
save_path = "./"


def main():
    # カメラのキャプチャを開始 --- (*1)
	cam = cv2.VideoCapture(0)

	cam.set(cv2.CAP_PROP_FPS, 10)           # カメラFPSを60FPSに設定
	cam.set(cv2.CAP_PROP_FRAME_HEIGHT, height) # カメラ画像の縦幅を240に設定
	cam.set(cv2.CAP_PROP_FRAME_WIDTH, width) # カメラ画像の横幅を320に設定

	# フレームの初期化 --- (*1)
	img1 = img2 = img3 = get_image(cam)
	th = 100
	num = 1
	while True:
		# ESCキーが押されたら終了
		if cv2.waitKey(1) == 0x1b: break
		# 差分を調べる --- (*2)
		diff = check_image(img1, img2, img3)
		# 差分がthの値以上なら動きがあったと判定 --- (*3)
		cnt = cv2.countNonZero(diff)
		if cnt > th:
			print("カメラに動きを検出")
			cv2.putText(img3,datetime.now().strftime("%Y/%m/%d %H:%M:%S"),(width-120,height-5),fontface,fontscale, color)
			cv2.imshow('PUSH ESC KEY', img3)
			# 写真を画像 --- (*4)
			#cv2.imwrite(save_path + str(num) + ".jpg", img3)
			num += 1
		else:
			cv2.imshow('PUSH ENTER KEY', diff)
		# 比較用の画像を保存 --- (*5)
		img1, img2, img3 = (img2, img3, get_image(cam))
	# 後始末
	cam.release()
	cv2.destroyAllWindows() 

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

# カメラから画像を取得する
def get_image(cam):
    img = cam.read()[1]
    #img = cv2.resize(img, (600, 400))
    return img
main()
