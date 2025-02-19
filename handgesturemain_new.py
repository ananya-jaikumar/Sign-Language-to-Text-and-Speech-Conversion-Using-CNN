# -*- coding: utf-8 -*-
"""
Created on Tue Jan 19 16:59:48 2021

@author: shrey
"""
import math
import cv2
import tensorflow as tf
import numpy as np
from gtts import gTTS
import os
from win32com.client import Dispatch


#language = 'en'

cap=cv2.VideoCapture(0)
minValue=70
class_names = [' ','is','am','Shreyas','this','I','my','project','can','we','made']# CEFHILOUVY,c=is,e=am,f=shreyas,h=this,l=my,o=project,u=can
json_file=open("model-11.5.json", "r")#v=we,y=made
model_json=json_file.read()
json_file.close()
model=tf.keras.models.model_from_json(model_json)
model.load_weights("model-11.5.h5")
str=""
prediction={}
for i in class_names:
    prediction[i]=0

while True:

    # Capture frames from the camera
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    # Get hand data from the rectangle sub window
    cv2.rectangle(frame, (370, 200), (570, 400), (255,0,0) ,1)
    roi = frame[200:400, 370:570]#200:400,370:570

    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray,(5,5),2)

    th3 = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,11,2)
    ret, res = cv2.threshold(th3, minValue, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

    x_test=cv2.resize(res,(200,200))
    pred=model.predict(x_test.reshape(1,200,200,1))
    current_symbol=class_names[np.argmax(pred[0])]

    prediction[current_symbol]+=1
    if prediction[current_symbol]>60:
        str+=current_symbol
        for i in class_names:
            prediction[i]=0
    sen=str.split()
    sen=" ".join(sen)
    print(sen)
    cv2.putText(frame, current_symbol, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2,(0,0,255), 2)
    cv2.putText(frame, str, (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1,(0,0,255), 2)
    cv2.imshow('image',frame)
    cv2.imshow('result',res)
    if cv2.waitKey(1) & 0xFF==ord('q'):
        break
#myobj = gTTS(text=sen, lang=language, slow=False)
#myobj.save("welcome.mp3")
#os.system("welcome.mp3")

speak = Dispatch("SAPI.SpVoice").Speak
speak(sen)
cap.release()
cv2.destroyAllWindows()
