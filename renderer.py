import ctypes
import datetime
import random
from PIL import ImageDraw, ImageFont, Image
import os
from functools import lru_cache
from datetime import datetime as dt

import PIL

class SmartWallpaperRenderer():
    
    """
        this is the biggest class
        
        renders the final wallpaper image with all the text on it.
    """
    
    def __init__(self, settings, screenSize) -> None:
        self.cycle = 0
        self.currDate = dt.today().strftime('%Y-%m-%d')
        self.getFont = lru_cache()(ImageFont.truetype)
        self.settings = settings
        self.font = settings["font"]
        self.fact = None
        self.joke = None
        self.screenSize = screenSize
        self.baseWallpaper = None
        self.initializeBaseWallpaper()
        self.currImage = None

    def mainLoop(self):
        self.renderTimeDate()
        self.renderFunFacts()
        self.renderJokes()
        self.renderFinalWallpaper()
        self.cycle += 1

    #Getting path to base wallpaper image
    def initializeBaseWallpaper(self):
        self.baseWallpaper = self.settings["wallpaper"]
        self.baseWallpaper = self.baseWallpaper.resize(self.screenSize)
        self.baseWallpaper.save(os.path.abspath("srcs") + "\BaseWallpaper.png")
        self.baseWallpaper = os.path.abspath("srcs") + "\BaseWallpaper.png"

    #printing the time and date on the image
    def renderTimeDate(self):
        #time/date will be positioned in the center, with plans to add more customizable options later.
        #coordinates in the PIL module start from the top left corner as the (0, 0) origin
        image = Image.open(self.baseWallpaper)
        imageText = ImageDraw.Draw(image)
        Time = datetime.datetime.now().time().strftime("%H:%M")
        if(self.currDate != dt.today().strftime('%Y-%m-%d')):
            self.currDate = dt.today().strftime('%Y-%m-%d')
        fontText = self.getFont(self.font, 150)
        fontDate = self.getFont(self.font, 50);
        w, h = fontText.getsize(Time) 
        wdate, hdate = fontDate.getsize(self.currDate)
        imageText.text((int((self.screenSize[0] - wdate)/2),int((self.screenSize[1]) + (2 * hdate))/2), self.currDate, font = fontDate)
        imageText.text((int((self.screenSize[0] - w)/2),int((self.screenSize[1] - (1.5 * h))/2)), Time, font=fontText)
        self.currImage = image

    def renderFunFacts(self):
        if(self.settings["facts"] != "yes"):
            return
        fontFact = self.getFont(self.font, 35)
        if(self.cycle % 15 == 0):
            factsFile = open(os.path.abspath("srcs/facts.txt"), "r")
            facts = factsFile.readlines()
            fact = facts[random.randint(0, len(facts))].split()
            currString = fact[0]
            currStringLen = 0
            hi = 550
            for i in range(1, len(fact)):
                currStringLen += fontFact.getsize(fact[i])[0]
                if(currStringLen >= hi):
                    hi += 550
                    currString += "\n" + fact[i]
                else:
                    currString += " " + fact[i]
            self.fact = currString
        w = fontFact.getsize_multiline(self.fact)[0]
        imageText = ImageDraw.Draw(self.currImage)
        imageText.text((int((self.screenSize[0] - fontFact.getsize("Did you know that:")[0])/2),int((self.screenSize[1] + 250)/2)), "Did you know that:", font=fontFact)
        imageText.text((int((self.screenSize[0] - w)/2),int((self.screenSize[1] + 350)/2)), self.fact, font=fontFact)

    def renderJokes(self):
        if(self.settings["jokes"] != "yes"):
            return
        fontJoke = self.getFont(self.font, 30)
        if(self.cycle % 30 == 0):
            jokesFile = open(os.path.abspath("srcs/jokes.txt"), "r")
            jokes = jokesFile.readlines()
            joke = jokes[random.randint(0, len(jokes))].split()
            currString = joke[0]
            currStringLen = 0
            hi = 400
            for i in range(1, len(joke)):
                currStringLen += fontJoke.getsize(joke[i])[0]
                if(currStringLen >= hi):
                    hi += 400
                    currString += "\n" + joke[i]
                else:
                    currString += " " + joke[i]
            self.joke = currString
        w = fontJoke.getsize_multiline(self.joke)[0]
        imageText = ImageDraw.Draw(self.currImage)
        imageText.text((int((self.screenSize[0] - fontJoke.getsize("Cringey dad joke:")[0])/2),int((self.screenSize[1] - 635)/2)), "Cringey dad joke:", font=fontJoke)
        imageText.text((int((self.screenSize[0] - w )/2),int((self.screenSize[1] - 550) /2)), self.joke, font=fontJoke)

    def renderFinalWallpaper(self):
        path = os.path.abspath("srcs") + "/finalImage.png"
        self.currImage.save(path)
        ctypes.windll.user32.SystemParametersInfoW(20, 0, path, 0)