# Candle
image trade candle to text

The goal of the project is to create a program for converting images of trading candles into text format.  (list of time, max, min).
Simple way for it is use cv2.findContours. Object detection and instance segmentation have bad image resolution 
when you need to detect more then 100 object and distance between each is 10-20 pxl ( i spend two monthes to understend it, but i learned a lot about image analysis ). 
Findcontours method requires removing or blurring unnecessary object other than candles, e.g. white background. 


ACCURACY: error 1-2 prices for 50% of candles. 1 point -- resolution error, i think. 1 point -- subtleties of rounding the result of calculations, i think.
