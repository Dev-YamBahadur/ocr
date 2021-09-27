from joblib.numpy_pickle_utils import xrange
import numpy as np

try:
    import Image, ImageEnhance, ImageFilter, ImageDraw
except ImportError:
    from openpyxl import Workbook
    import PIL.Image
    from PIL import ImageEnhance
    from PIL import ImageDraw
    from wand.image import Image
    from googletrans import Translator
import pytesseract
import cv2
from openpyxl.utils.dataframe import dataframe_to_rows
import string
import simplejson
import pandas as pd
import os

# Declatation
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\yamku\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'
image_name = "id.jpg"
threshold = 140
table = []

for i in range(256):

    if i < threshold:

        table.append(0)
    else:

        table.append(1)


def read_text_file(file_path):
    with open(file_path, 'r') as f:
        print(f.read())


def text_to_column():
    print("_________________User Details___________________")

    # if text.find("名") :
    namex = text.find("名") + 1
    # if text.find("性",namex) :
    namey = text.find("性", namex) - 1
    # if namex >0 and namey > namex:
    #     user['name']=  text[namex:namey]

    if text.find("男") > 0:
        gender = "Male 男 "

    if text.find("女") > 0:
        gender = "Female 女"

    if text.find("汉") > 0:
        nationality = "CHINESE 汉"
    month = text[text.find("年") + 1:text.find("月")]
    number = []
    # tex2=text.split(" ")
    for ch in text.split():
        if len(ch) > 10:
            number.append(ch)

    # yyx,yyx =0
    # if text.find("出生"):
    #     yyx = text.find("出生")
    # elif text.find("出 生"):
    #     yyx= text.find("出 生")
    # if text.find("年") :
    #     yyy = text.find("年")
    # if yyx and yyy >0 :
    #     temp  =text[yyx+1:yyy-1]
    #     for c in temp:
    #         if len(user['year']) < 4:
    #             if c.isdigit():
    #                 user['year'] = user['year'] + c
    #
    # elif yyx>0 :
    #     user['year']=text[yyx+1:4]
    #
    #
    pointer = ""
    translater = Translator()
    eng_name = "blank"
    # eng_name = translater.translate(text[namex:namey], dest='en')
    year = text[text.find("生"):text.find("年")]
    YY = ""
    for c in year:
        if len(YY) < 4:
            if c.isdigit():
                YY = YY + c

    month = text[text.find("年"): text.find("月")]
    MM = ""
    for m in month:
        if m.isdigit():
            if len(MM) < 2:
                if m.isdigit():
                    MM = MM + m

    DD = ""
    if text[text.find("月"):text.find("日")]:
        day = text[text.find("月"):text.find("日")]
        for d in day:
            if d.isdigit():
                if len(DD) < 2:
                    if d.isdigit():
                        DD = DD + m

    else:
        DD = "unrecognized"
    address = text[text.find("佳 址") + 1:text.find("公民身份证号昼") - 1]
    # --------------------------PRINTING--------------------------------------------------------#
    print("Name :- ", text[namex:namey] + translater.translate(text[namex:namey], dest='en').text,
          "\n Nationality :-", nationality, ",",
          "\n Gender :-", gender, ",",
          "\n DOB :-",
          YY, "-", MM, "-", DD,
          "\n Address :-",
          address.strip(),
          #      ",\n English Add :-  ",translater.translate(address.strip(), dest='en').text,
          ",\n Citizen ID number",
          # ",\n Citizen ID number", text[text.find("号码") + 7]
          number
          # text.split("", 1)[0]
          )


# print("---------------------------------raw data ---------------------------------------------------\n ",text,"\n ---------------------------------raw data ---------------------------------------------------",translater.translate(text2).text)


def getPixel(image, x, y, G, N):
    L = image.getpixel((x, y))
    if L > G:
        L = True
    else:
        L = False

    nearDots = 0
    if L == (image.getpixel((x - 1, y - 1)) > G):
        nearDots += 1
    if L == (image.getpixel((x - 1, y)) > G):
        nearDots += 1
    if L == (image.getpixel((x - 1, y + 1)) > G):
        nearDots += 1
    if L == (image.getpixel((x, y - 1)) > G):
        nearDots += 1
    if L == (image.getpixel((x, y + 1)) > G):
        nearDots += 1
    if L == (image.getpixel((x + 1, y - 1)) > G):
        nearDots += 1
    if L == (image.getpixel((x + 1, y)) > G):
        nearDots += 1
    if L == (image.getpixel((x + 1, y + 1)) > G):
        nearDots += 1

    if nearDots < N:
        return image.getpixel((x, y - 1))
    else:
        return None


# G: Integer image binarization threshold
# N: Integer Noise reduction rate 0 <N <8
# Z: Integer Noise reduction times
# Output
# 0: Noise reduction succeeded
# 1: Noise reduction failed

def filterNoise(image, G, N, Z):
    draw = ImageDraw.Draw(image)
    for i in xrange(0, Z):
        for x in xrange(1, image.size[0] - 1):
            for y in xrange(1, image.size[1] - 1):
                color = getPixel(image, x, y, G, N)
                if color != None:
                    draw.point((x, y), color)


def read_file(filename):
    img = cv2.imread(filename)
    #    text2 = pytesseract.image_to_string(img, 'chi_sim')
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.medianBlur(img, 3)
    text = pytesseract.image_to_string(img, 'chi_sim')
    workbook = Workbook()
    spreadsheet = workbook.active
    spreadsheet["A1"] = "data"
    # Append column names first
#    spreadsheet.append(["Converted Data"])
    spreadsheet.append(text.split())
    workbook.save(filename="output.xlsx")


def opencv():
    img = cv2.imread("ob.jpg")
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.medianBlur(img, 3)
    bin = cv2.threshold(img, 182, 255, cv2.THRESH_BINARY)
    img = cv2.bitwise_not(bin)

    text = pytesseract.image_tostring(img)


def excel(fname, crud, data, ):
    fname = fname
    data = pd.read_excel(data)
    workbook = Workbook()
    spreadsheet = workbook.active
    spreadsheet["A1"] = "data"
    # Append column names first
    spreadsheet.append(["Converted Data"])
    spreadsheet.append(data)
    workbook.save(filename="output.xls")


def main():
    name = 'NA',
    gender = 'NA',
    year = "",
    month = "",
    day = "",
    nationality = 'NA',
    address = "",

    # Folder Path
    path = "C:/Users/yamku/PycharmProjects/OCR"
    os.chdir(path)
    for file in os.listdir():
        # Check whether file is in text format or not
        if file.endswith(".jpg" or ".JPEG" or ".png" or ".PNG"):
            file_path = f"{path}\{file}"
            # call read text file function
            read_file(file_path)
    # Im = PIL.Image.open(image_name)
    # Im = PIL.Image.open(image_name).convert('L')  # Convert to grayscale
    # Im.save('g_' + image_name)
    # Im = Im.point(table, '1')
    # Im.save('b_' + image_name)
    # #  enhancer = ImageEnhance.Contrast(Im)  # Comment this while use Strongly Filter
    #    Im.save('Treated.jpg')
    # text = pytesseract.image_to_string(Im, 'chi_sim')

    # ret, bin = cv2.threshold(img, 182, 255, cv2.THRESH_BINARY)
    # img = cv2.bitwise_not(bin)
    # sharpen_kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    # img = cv2.filter2D(img, -1, sharpen_kernel)


if __name__ == '__main__':
    main()
