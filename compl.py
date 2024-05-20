from ultralytics import YOLO
import cv2
import numpy as np
from gpiozero import LED
import RPi.GPIO as GPIO
from time import sleep
#config motor PWM
led1= LED(14)
led2= LED(4)
led3= LED(17)
GPIO.setmode(GPIO.BCM)
enA = 13
enB = 12
GPIO.setup(enA,GPIO.OUT)
GPIO.setup(enB,GPIO.OUT)

frequency = 50
pwm1=GPIO.PWM(enA,frequency)
pwm2=GPIO.PWM(enB,frequency)

pwm1.start(0)
pwm2.start(0)

led1.on()
led2.off()
led3.on()
led4.off()

model = YOLO("/home/vinhpi/Desktop/bet.pt")
file_path='/home/vinhpi/Desktop/images/frame.jpg'

def process_image(file_path):

    cap=cv2.VideoCapture(0)
    cap.set(3, 480)
    cap.set(4, 640)    
    ret, frame = cap.read() 
    results=model(frame,show=True)
    for r in results:
        array=r.boxes.cls.numpy()
        print(array)
        total = np.sum(array)
        print("Total:", total)
    if total == 1:
        print("redlight")
        pwm1.ChangeDutyCycle(100)
        pwm2.ChangeDutyCycle(100)
    if total == 4:
        print("yellowlight")
        pwm1.ChangeDutyCycle(0)
        pwm2.ChangeDutyCycle(0)
    if total == 5:
        print("greenlight")
        for duty in range(100,-1,-5):
            pwm1.ChangeDutyCycle(duty)
            pwm2.ChangeDutyCycle(duty)
            sleep(0.5)
    if ret:
        cv2.imshow('Camera Output', frame)
        cv2.waitKey(1)
        cv2.imwrite(file_path, frame)
        print(f"Ảnh đã được lưu tại {file_path}")
    else:
        print("Không thể đọc dữ liệu từ camera") 
    cap.release()
    cv2.destroyAllWindows()   
     
while True:
    process_image(file_path)
    sleep(1)




