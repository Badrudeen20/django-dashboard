import random
from .models import *


def seed_db(n=20) -> None:
    try:
        for i in range(0,n):
           
            name ='Loki 2023 S02E03 Dual Audio ORG Hindi 720p HDRip 750MB ESubs',
            image= 'https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgINFunvdxlAd8qjJUAsxfRvNN81T02DVWiDw76E4jxJeQv_0d7uEdQnXtLio2agiSRdh24SsvRzMGWnfW2C_V4ce_Ihn1DsdPnypPVrUthyBPoZv9qwI9pQnquG2q5aJ-HsYqwTUQM5rfAXYnk8oCLYvtGNPatrEWTPjEh3JnWjcwg-VDAMkm_lpBjqg/s225/sec.jpg',
            rate = random.randint(1, 10),
            size = random.randint(300, 900),
            lang ='Hindi,English',
            genre='Action,Comedy',
            story= 'The script enters an infinite loop that iterates through angles from 0 to 360 degrees in 5-degree increments, calculating the new mouse position based on the current angle and then moving the mouse to that position using pyautogui.moveTo(). You can adjust the parameters to change the size and speed of the circular motion.'
            
            
            post_obj = Posts.objects.create(name=name,image=image,rate=rate,size=size,lang=lang,genre=genre,story=story)
    
    except Exception as e:
        print(e)