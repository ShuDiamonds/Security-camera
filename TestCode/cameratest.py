# -*- Coding: utf-8 -*-
import cv2
# カメラのキャプチャを開始 --- (*1)
cam = cv2.VideoCapture(0)

cam.set(cv2.CAP_PROP_FPS, 10)           # カメラFPSを60FPSに設定
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 240) # カメラ画像の縦幅を720に設定
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 320) # カメラ画像の横幅を1280に設定

print(cam.get(cv2.CAP_PROP_FPS))
print(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
print(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))

while True:
    # 画像を取得 --- (*2)
    _, img = cam.read()
    # ウィンドウに画像を表示 --- (*3)
    cv2.imshow('PUSH ESC KEY', img)
    # escキーが押されたら終了する
    if cv2.waitKey(1) == 0x1b: break
# 後始末
cam.release()
cv2.destroyAllWindows()
