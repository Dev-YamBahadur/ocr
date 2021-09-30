from __future__ import print_function
import cv2
import easyocr
import numpy
import pytesseract

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
    faces = face_cascade.detectMultiScale(frame_gray)
    for (x, y, w, h) in faces:
        center = (x + w // 2, y + h // 2)
       #frame = cv2.ellipse(frame, center, (w // 2, h // 2), 0, 0, 360, (255, 0, 255), 4)

        faceROI = frame[y:y + h, x:x + w]

    cv2.imwrite('face.jpg', faceROI)



def text_reader(img):
    reader = easyocr.Reader(['ch_sim'], gpu=False)
    output = reader.readtext(img, detail=0)
    print(output)


if __name__ == '__main__':
    image = cv2.imread('1.jpg')
    text_reader(image)
    face_reader(frame=image)
