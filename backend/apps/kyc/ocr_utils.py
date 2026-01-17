import pytesseract
import cv2
import os
import numpy as np

TESSERACT_PATH = r"C:\Users\ISU_845\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"

if not os.path.exists(TESSERACT_PATH):
    raise RuntimeError("Tesseract executable not found at given path")

pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH


def extract_text(image_path):
    image = cv2.imread(image_path)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)[1]

    custom_config = r'--oem 3 --psm 6'
    text = pytesseract.image_to_string(gray, config=custom_config)

    return text