import pytesseract
from pytesseract import Output
from PIL import Image
import cv2
import time
import selenium
import cv2
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import albumentations as A
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
import numpy as np
import re

driver = webdriver.Chrome()
driver.maximize_window()
driver.get("https://monkeytype.com/")
driver.refresh()
elem =WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button.active.acceptAll')))
elem.click()
driver.refresh()


def find_text_init():
    elem =WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[9]/div[2]/main/div/div[3]/div[8]/div[3]')))
    driver.save_screenshot('/Users/umang/Desktop/test.png')

    img = '/Users/umang/Desktop/test.png'
    
    
    # im = Image.open(img)
    # width, height = im.size
    # top = height / 2.25

    # bottom =  height /1.7
    # im1 = im.crop((350, top, 2850, bottom))
    # im1.save(img) 
    
    mg = cv2.imread(img)
    
    #mg = cv2.cvtColor(mg, cv2.COLOR_BGR2GRAY)
   
    # cv2.imshow('test.png', thresh, )
    lower = np.array([22, 93, 0])
    upper = np.array([45, 255, 255])
    imgHSV = cv2.cvtColor(mg, cv2.COLOR_BGR2HSV)
    # create the Mask
    mask = cv2.inRange(imgHSV, lower, upper)
    # inverse mask
    mask = 255-mask
    res = cv2.bitwise_and(mg, mg, mask=mask)
    ret, thresh = cv2.threshold(res, 65, 255, cv2.THRESH_BINARY_INV)
    cv2.imshow("mask", mask)
    cv2.imshow("cam", mg)
    cv2.imshow('res', res)
    cv2.imwrite( img, thresh)
    img_path1 = '/Users/umang/Desktop/test.png'
 
    text = pytesseract.image_to_string(img_path1,lang='eng')
    text_3 = text
    start = text.find('@ english')
    end = text.find('Cc')

    text = text[start+10:end]
    if(text[0]=='l'):
        text=text[2:]
    text.replace("\ne\n", "")
    return text, text_3
text, _ = find_text_init()
# start = text.find('@ english')
# end = text.find('Cc')

# text = text[start+10:end]
# if(text[0]=='l'):
#     text=text[2:]
space = text.find(" ")
text_sample = text
text = text.replace("\n", " ")
first_word=text[:space]
def find_text():
    _, text = find_text_init()
    start = text.find('@ english')
    end = text.find('Cc')
    text = text[start+12: end]
    text2 = text
    text = text.replace('\n', ' ')
    
    
    
    
    return text, text2


#print(f'{text}\n')
actions = ActionChains(driver)
count = 0
words = ""
words = words+text
word_sample = ""
word_sample = word_sample+text_sample
a = len(words)
i = 0
while a!=0:
   
    actions.send_keys(words[i])
    actions.perform()
    WebDriverWait(driver, 12)
    if(word_sample[i]=="\n"):
       count =count +1
       if(count==2):
        new_text, _ = find_text()
        a = new_text[0:10]
        beg = words.find(a)
        words = words[:beg]
        words = words+new_text
        f, g = find_text()
        a = g[0:10]
        beg = word_sample.find(a)
        word_sample = word_sample[:beg]
        word_sample=word_sample+g


        
        count = 0
        a = len(words)
    #print(words)
    i = i+1
        
        




cv2.waitKeyEx(5)


 
# Displaying the output image
# cv2.imshow('Truncate Threshold', thresh)
# reader = easyocr.Reader(['en'])
# result = reader.readtext('/Users/umang/Desktop/test.png', detail = 0)
# print(result)
'''or she well large by problem part between hand say be up little no good follow could
should do turn but for know run number present they with head get during after only
 house stand long still will real who way person great she out seem since world man'''