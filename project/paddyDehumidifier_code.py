
    #import library สำหรับตรวจจับตัวเลขบนเครื่องวัดความชื้น

import imutils
import cv2
import numpy as np
from matplotlib import pyplot as plt
import re
import array as arr
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import pyrebase

    # import library raspi
import time
import RPi.GPIO as GPIO
import board
import adafruit_shtc3
import random
import os
import picamera
from gpiozero import Buzzer
from time import sleep

buzzer = Buzzer(17)
RELAIS_1_GPIO = 14
ENA = 23
in1 = 24
in2 = 25
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(ENA, GPIO.OUT)
GPIO.setup(in1, GPIO.OUT)
GPIO.setup(in2, GPIO.OUT)
GPIO.output(in1, GPIO.LOW)
GPIO.output(in2, GPIO.LOW)
PWM = GPIO.PWM(ENA, 1000)
PWM.start(100)
GPIO.setup(RELAIS_1_GPIO, GPIO.OUT) # GPIO Assign mode
GPIO.output(RELAIS_1_GPIO, GPIO.HIGH)

file_name = "image.jpg"

def picturePath(file_name):
    with picamera.PiCamera() as camera:
        camera.resolution = (2592, 1944)
        camera.framerate = 15
        camera.start_preview()
        sleep(2)
        camera.capture(file_name)
        camera.stop_preview()
        path = '/home/pi/Desktop/image.jpg'
        return path

def croppedDigits(path):
    def displayImg(name, image):
        cv2.imshow("{}".format(name), image)
        cv2.waitKey(0)

    def save_image_with_path(image, path, filename):
    # ตรวจสอบว่าพาธที่ระบุมีหรือไม่
        if not os.path.exists(path):
            os.makedirs(path)

        # บันทึกรูปภาพ
        full_path = os.path.join(path, filename)
        cv2.imwrite(full_path, image)

    image = cv2.imread(path)
    image = imutils.resize(image, height = 500)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.blur(gray, (15, 15))
    bbox_x = arr.array('i', [214])  #วางกรอบแต่ละบ็อกของ Digits ทั้งหมด 3 บ็อก
    bbox_y = arr.array('i', [211])
    bbox_w = arr.array('i', [247-214])
    bbox_h = arr.array('i', [290-211])

    DIGITS_LOOKUP = {
        (1, 1, 1, 0, 1, 1, 1): 0,
        (0, 0, 1, 0, 0, 1, 0): 1,
        (1, 0, 1, 1, 1, 0, 1): 2,
        (1, 0, 1, 1, 0, 1, 1): 3,
        (0, 1, 1, 1, 0, 1, 0): 4,
        (1, 1, 0, 1, 0, 1, 1): 5,
        (1, 1, 0, 1, 1, 1, 1): 6,
        (1, 1, 1, 0, 0, 1, 0): 7,
        (1, 1, 1, 1, 1, 1, 1): 8,
        (1, 1, 1, 1, 0, 1, 1): 9,
    }
    digits = []


    titles = ['Image', 'gray']
    images = [image, gray]
    
    for i in range(2):
        plt.subplot(2,2,i+1),plt.imshow(images[i],'gray')
        plt.title(titles[i])
        plt.xticks([]),plt.yticks([])
    plt.show()

    for i in range(len(bbox_x)): #ลูปตามจำนวนใน bbox_x
        frame = gray
        frame_copy = blurred.copy()
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (35, 30))
        thresh = cv2.morphologyEx(frame, cv2.MORPH_BLACKHAT, kernel)
        displayImg("thresh", thresh)
        thresh = cv2.threshold(thresh, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
        displayImg("thresh", thresh)
        thresh = cv2.threshold(thresh, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1] #ทำให้รูปเปลี่ยนเป็นสีตรงข้าม (ขาว - ดำ)
        displayImg("thresh", thresh)
        (x, y, w, h) = (bbox_x[i], bbox_y[i], bbox_w[i], bbox_h[i])
        roi1 = thresh[y:y + h, x:x + w]

        #---------Digits แต่ละส่วน ทั้งหมด 7 ส่วน---------
        segments = [
            ((10, 0), (20, 10)), #top 
            ((0, 0), (10, h // 2)),	# top-left
            ((w - 10, 0), (w, h // 2)),	# top-right
            ((10, (h // 2)) , (20, (h // 2) + 5)), # center
            ((0, h // 2), (10, h)),	# bottom-left
            ((w - 10, h // 2), (w, h)),	# bottom-right
            ((10, h - 10), (20, h))	# bottom
        ]
        on = [0] * len(segments) #len คือ แต่ละส่วนของ Digits Ex. top, top-left, center .. etc 7 parts in function

        #-------------เอาไว้เช็คแต่ละส่วนของ Digits--------------
        for (i, ((xA, yA), (xB, yB))) in enumerate(segments):
            segROI = roi1[yA:yB, xA:xB]
#             print("SegRoi : ", segROI)
            total = cv2.countNonZero(segROI)
            show = cv2.rectangle(roi1, (xA, yA), (xB, yB), (127, 127, 127), cv2.FILLED) #เอาไว้เช็คตำแหน่ง ที่กำลังตรวจจับ Digits
            cv2.imshow("Show Roi2", show)
            save_image_with_path(show, "E:\\09_Projects\\Piece", f"image_{i}.png") #Save path
            cv2.imwrite(f"result_{i}.jpg", show) 
            cv2.waitKey(0)
#             print(i, " total", total) //สำหรับเช็คค่า
            area = (xB - xA) * (yB - yA)
#             print("area", area) //สำหรับเช็คค่า
            area = (xB - xA) * (yB - yA)
            print("total / area = ", total / float(area))

            if total / float(area) > 0.5:
                on[i] = 1

        digit = DIGITS_LOOKUP[tuple(on)]
        digits.append(digit)

        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 1)
        cv2.putText(frame, str(digit), (x - 10, y + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 255, 255), 2)

        if cv2.waitKey(1) & 0xFF == 27:
            break

#     displayImg("Output", frame)
    v = "{}{}{}".format(digits[0], digits[1], digits[2])
    integer_humd = int(v) 
    print(v)

    config = {
        "apiKey": "apiKey",
        "authDomain": "authDomain.firebaseapp.com",
        "databaseURL": "DATABASE_URL",
        "projectId": "PROJECT_ID",
        "storageBucket": "STORAGE_BUCKET",
        "messagingSenderId": "MESSAGING_ID",
        "appId": "APP_ID",
        "measurementId": "MEASUREMENT_ID"
        
        }

    firebase = pyrebase.initialize_app(config)

    db = firebase.database()

    # เชื่อมต่อ Firebase Realtime Database
    data = {
        "humidity" : integer_humd
        }
    
    db.child("DHT").set(data)
    
    # กำหนดไฟล์การกำหนดค่า Firebase Admin SDK
    cred = credentials.Certificate('PATH_SERVICE_ACCOUNT_KEY')

    # กำหนดคอนฟิก Firebase
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'DATABASE_URL'
    })

    # เชื่อมต่อ Firebase Realtime Database
    ref = db.reference('/DHT/humidity')

    ref.set(integer_humd)

    cv2.destroyAllWindows()

    print(u"{}{}.{} %".format(digits[0], digits[1], digits[2]))
    text = u"{}{}{} %".format(digits[0], digits[1], digits[2])
    cv2.destroyAllWindows() # destroys the window showing image
    humd = int(re.search(r'\d+', text).group())
    print(humd)
    return humd

def tempDetect():
    print("________tempDetection________")
    i2c = board.I2C()   # uses board.SCL and board.SDA
    sht = adafruit_shtc3.SHTC3(i2c)
    temperature, relative_humidity = sht.measurements
    
    config = {
        "apiKey": "apiKey",
        "authDomain": "authDomain.firebaseapp.com",
        "databaseURL": "DATABASE_URL",
        "projectId": "PROJECT_ID",
        "storageBucket": "STORAGE_BUCKET",
        "messagingSenderId": "MESSAGING_ID",
        "appId": "APP_ID",
        "measurementId": "MEASUREMENT_ID"
    }

    firebase = pyrebase.initialize_app(config)

    db = firebase.database()

    # เชื่อมต่อ Firebase Realtime Database
    data = {
        "TEMP" : temperature,
        "HUMD" : relative_humidity
        }
    
    db.child("SHTC3").set(data)
    
    print("Temperature: %0.1f C" % temperature)
    print("Humidity: %0.1f %%" % relative_humidity)
    print("")
    
    return temperature

def tankRotation(boolean):
    print("-------- Function ON --------- tankRotation --------")
    ENA = 23
    in1 = 24
    in2 = 25

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(ENA, GPIO.OUT)
    GPIO.setup(in1, GPIO.OUT)
    GPIO.setup(in2, GPIO.OUT)
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.LOW)
    PWM = GPIO.PWM(ENA, 1000)
    PWM.start(100)

    if(boolean == True):
        print("_________________ROTATING________________")
        GPIO.output(in1, GPIO.HIGH)
        GPIO.output(in2, GPIO.LOW)
    elif(boolean == False):
        print("_________________STOP________________")
        GPIO.output(in1, GPIO.LOW)
        GPIO.output(in2, GPIO.LOW)

cred = credentials.Certificate('PATH_SERVICE_ACCOUNT_KEY')  # เปลี่ยนเป็นที่อยู่ของไฟล์ serviceAccountKey.json
firebase_admin.initialize_app(cred, {
    'databaseURL': 'DATABASE_URL'  # เปลี่ยนเป็น URL ของฐานข้อมูล Firebase Realtime Database
})

readStatus = db.reference('/button_state')
# ตรวจสอบค่าจาก Firebase และควบคุม GPIO ตามค่าที่ได้

Start = True
while Start:
        state = readStatus.get()
        if state == 'กดหยุด':
            tempValue = tempDetect()
            value = croppedDigits(picturePath(file_name))
        #     checkPath = picturePath()
            if(value > -1):
                print("_________________PASS________________")
                print("________TANK HAS BEEN ROTATING_______")
                GPIO.output(in1, GPIO.HIGH)
                GPIO.output(in2, GPIO.LOW) #เครื่องหมุน
                if(tempValue > 40):
                    GPIO.output(RELAIS_1_GPIO, GPIO.HIGH)
                    buzzer.on()
                    sleep(1)
                    buzzer.off()
                    sleep(1)
                elif(tempValue <= 40):
                    GPIO.output(RELAIS_1_GPIO, GPIO.LOW)
                time.sleep(30)
            elif(value <= -1):
                print("______________NOT PASS_____________")
                print("_______TANK HAS BEEN STOPING_______")
                GPIO.output(in1, GPIO.LOW)
                GPIO.output(in2, GPIO.LOW) #เครื่องหยุด
                GPIO.output(RELAIS_1_GPIO, GPIO.HIGH)
        elif state == 'กดเริ่ม':
            print("_______TANK HAS BEEN STOPING_______")
            GPIO.output(in1, GPIO.LOW)
            GPIO.output(in2, GPIO.LOW) #เครื่องหยุด
            GPIO.output(RELAIS_1_GPIO, GPIO.HIGH)
    

croppedDigits("E:\\09_Projects\\result\\0.jpg")

##https://www.youtube.com/watch?v=CtKu3hMjxSY -- Project Video Presentation
