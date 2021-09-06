import time
import numpy as np
import datetime
import csv

import cv2


# input data besides screen
time = datetime.datetime(2021, 8, 25, 16, 30)       # note: year, month, day, hour, minute
cndl_frame = datetime.timedelta(minutes=15)
max_price = 33562
min_price = 32127

start = time - cndl_frame

#__________________________________________________________________________________________________________________
def candle_cnts(image):
    """ Find contours.
    Input -- a grayscale image is needed, if not, use it : image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    cv2.threshold -- translate into binary format. Black 0,0,0 and  255, 255, 255. 
        One for the needed, the other for the unnecessary. Сontrolled by parameter cv2.THRESH_...
        cv2.THRESH_BINARY for light background and cv2.THRESH_BINARY_INV for black background. 
        Play with parametr number 2, for delate pale elementes from image. 
        If background is black, that mean there are not pale elementes. Use 10 or less.
    
    cv2.findContours -- find contours.
        The image should not have bright or clear unnecessary elements.
        cv2.RETR_EXTERNAL -- sorted outside contours only
    
    cv2.drawContours -- visualization and storage for control. """
    
    T, thresh_img = cv2.threshold(image, 100, 255, cv2.THRESH_BINARY_INV)
    
    contours, _ = cv2.findContours(thresh_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    
    img_contours = np.zeros(image.shape)
    cv2.drawContours(img_contours, contours, -1, (255,0,0), 1)
    cv2.putText(img_contours, str(len(contours)), (20,20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2)
    cv2.imwrite('F:\Python/candle/cndl_all.jpg', img_contours)

    return contours


def sort_left_to_right(cndls):
    """ Sorted contours by left to right """
    first_coord_list = [i[0][0][0] for i in cndls]
    
    first_coord_list.sort()

    for x in first_coord_list:  
        for i in cnts:
            if x == i[0][0][0]: 
                cndl_list.append(i)
    
    return cndl_list

def find_coord_mm(max, min):
    """ Find coordinate of max and min price of screen. 
    cv2.drawContours -- visualization and storage for control . """
    
    cnt_max = []
    cnt_min = []
    max_pxl = cndl_list[0][0][0][1]
    min_pxl = cndl_list[0][0][0][1]
    for i in cnts:
        if i[0][0][1] < max_pxl: 
            max_pxl = i[0][0][1]
            cnt_max = i
        for x in i:
            if x[0][1] > min_pxl: 
                min_pxl = x[0][1]
                cnt_min = i
    
    cv2.drawContours(image, [cnt_max, cnt_min], -1, (0,255,255), 2)
    cv2.imwrite('F:\Python/candle/cndl_mm.jpg', image)
  
    return max_pxl, min_pxl


def jump_time():
    """ Accounting of non-working hours.
    for the future -- accounting holidays and transfer of working days  (website?). """

    tmp = start + cndl_frame
    ses_end = datetime.time(18, 45)
    work_end = datetime.time(23, 50)
    
    if tmp.time() == ses_end:
        tmp = tmp.replace(hour=19, minute=0)

    if cndl_frame!=datetime.timedelta(days=1) and (tmp.time()>work_end or tmp.date()>start.date()):
        tmp = tmp.replace(hour=7, minute=0)
        hol = tmp.weekday()
        if hol == 5: 
            tmp = tmp + datetime.timedelta(days=2)

    return tmp
#_______________________________________________________________________________________________________________

class Candle:
    max_pc = None
    min_pc = None
    time = None

    def __init__(self, cndl_cnt):
        self.cndl_cnt = cndl_cnt

    def calculation(coord):
        """ Formulas for calculation. 
        а -- displacement of max/min of the pixel relative to max_pxl expressed in %
        с -- displacement in% translate to price point
        Then we round up to the required sign. The template is the price values taken from the screen.
        mm -- subtract the difference from the point relative to which the offset was considered, which gives the desired price
        """
        
        a = float(((coord - max_pxl) * 100) / (min_pxl - max_pxl))
        b = float(max_price - min_price)
        c = float(((b) * a) / 100)
       
        if type(max_price) == int: 
            c = round(c) 
        else:
             s = str(max_price)
             c = round(c, abs(s.find('.')-len(s))-1)
            
        mm = max_price - c
        return mm


    def calculation_max_min(self, cnt):
        """ Calculation max min.
        Find coordinate of max and min point and go to formulas for calculation. """
        
        x = cnt[0][0][1]
        y = 0
        for i in cnt:
            if i[0][1] > y: 
                y = i[0][1]
        max = max_price
        min = min_price
        
        if x != max_pxl: 
            max = Candle.calculation(x)
        if y != min_pxl: 
            min = Candle.calculation(y)
        
        return max, min


#_______________________________________________________________________________________________________________

image_path = 'F:\Python/candle/test.jpg'
image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE) # need cv2.IMREAD_GRAYSCALE
cnts = candle_cnts(image)
 
cndl_list = []
cndl_list = sort_left_to_right(cnts)

max_pxl, min_pxl = find_coord_mm(max_price, min_price)

data_list = []
for i in cndl_list:
    x = Candle(i)
    x.max_pc, x.min_pc = x.calculation_max_min(i)
    x.time = jump_time()

    start = x.time

    data_list.append(x)

name = time.strftime('%Y-%m-%d-%H-%M')
with open (name + ".txt", 'w') as f:
    write = csv.writer(f)
    for i in data_list:
        write.writerow( [i.time, i.max_pc, i.min_pc] )         # ?? i.cndl_cnt 

print(data_list[0].time, data_list[0].max_pc, data_list[0].min_pc, )

# ACCURACY: error of 1-2 price points with a 4-5 digit price value (30,000). 