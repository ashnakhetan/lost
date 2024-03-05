from PIL import Image
import pytesseract
import os
import openai

txt_path = 'cropped_images.txt'

# If you don't have tesseract executable in your PATH, include the following:
pytesseract.pytesseract.tesseract_cmd = r'/usr/local/bin/tesseract'

# Batch processing with a single file containing the list of multiple image file paths
ocr_text = pytesseract.image_to_string(txt_path)

with open('output.txt', 'w') as file:
    file.write(ocr_text)


