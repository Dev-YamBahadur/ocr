from __future__ import print_function

import cv2
import easyocr
import numpy
import pytesseract
from googletrans import Translator

pytesseract.pytesseract.tesseract_cmd = r'C:\Users\yamku\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'


def face_reader(frame):
    face_cascade_name = 'data/haarcascades/haarcascade_frontalface_alt.xml'
    face_cascade = cv2.CascadeClassifier()
    if not face_cascade.load(cv2.samples.findFile(face_cascade_name)):
        print('--(!)Error loading face cascade')
        exit(0)

    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame_gray = cv2.equalizeHist(frame_gray)
    # -- Detect faces
    faceROI = cv2.imread('user.jpg')
    faces = face_cascade.detectMultiScale(frame_gray)
    for (x, y, w, h) in faces:
        center = (x + w // 2, y + h // 2)
        # frame = cv2.ellipse(frame, center, (w // 2, h // 2), 0, 0, 360, (255, 0, 255), 4)

        faceROI = frame[y:y + h, x:x + w]
    cv2.imwrite('face.jpg', faceROI)

    # Write Image  in workbook
    # wb = openpyxl.Workbook()
    # ws = wb.worksheets[0]
    # img = openpyxl.drawing.image.Image('test.jpg')
    # img.anchor = 'A1'
    # ws.add_image(img)
    # wb.save('out.xlsx')


def text_reader(img):
    reader = easyocr.Reader(['ch_sim'], gpu=False)
    output = reader.readtext(img, detail=0)
    # print(output)
    return output


if __name__ == '__main__':
    image = cv2.imread('8.jpeg')
    text = text_reader(image)
    face_reader(frame=image)
    print(text)
    NoneType = type(None)
    translate = Translator()
    for j, char in enumerate(text):
        # for i,c in enumerate(char):
        #     if c== '男':
        #         #print(j,i)
        #         print(translate.translate(c,dest='en').text)
        #     # if c=='芏':
        #     #     if j+1
        if char != '':
            if translate.translate(char, dest='en').text:
                print(translate.translate(char, dest='en').text)
