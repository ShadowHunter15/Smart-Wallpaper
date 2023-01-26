import ctypes
import datetime
import random
from PIL import ImageDraw, ImageFont, Image
import os
from functools import lru_cache
import psutil
class SmartWallpaperRenderer():
    
    """
        this is the biggest class
        
        renders the final wallpaper image with all the text on it.
    """
    
    def __init__(self, settings, screenSize) -> None:
        print("RENDERER: GO")
        self.ratio =  screenSize[0] / 1366
        self.getFont = lru_cache()(ImageFont.truetype)
        print(self.ratio)
        self.cycle = 0
        self.settings = settings
        self.font = settings["font"]
        self.fact = None
        self.joke = None
        self.screenSize = screenSize
        self.baseWallpaper = None
        self.initializeBaseWallpaper()
        self.initilalizeVariables()
        self.currImage = None
        self.ping = "Infinte"
        self.rate = "--"
    
    #things that have to be updated every loop.
    def mainLoop(self, cycle):
        self.cycle = cycle
        self.renderFunFacts()
        self.renderJokes()
        self.renderBattery()
        self.renderInternetPing(self.ping)
        self.renderChargingRate(self.rate)
    #Getting path to base wallpaper image
    
    def initializeBaseWallpaper(self):
        if(self.settings["wallpaper"][1] == "img"):
            self.baseWallpaper = self.settings["wallpaper"][0]
        else:
            self.baseWallpaper = Image.open(random.choice(self.settings["wallpaper"][0]))
        self.baseWallpaper = self.baseWallpaper.resize(self.screenSize)
        
        self.baseWallpaper.save(os.path.abspath("srcs") + "\BaseWallpaper.png")
        self.baseWallpaper = os.path.abspath("srcs") + "\BaseWallpaper.png"

    #printing the time and date on the image
    def renderTimeDate(self, Time, currDate):
        #time/date will be positioned in the center, with plans to add more customizable options later.
        #coordinates in the PIL module start from the top left corner as the (0, 0) origin
        image = Image.open(self.baseWallpaper)
        imageText = ImageDraw.Draw(image)
        PMorAM = datetime.datetime.now().time().strftime("%p")
        fontTime = self.getFont(self.font, int(150 * self.ratio))
        fontDate = self.getFont(self.font, int(50 * self.ratio));
        wt, ht = fontTime.getsize(Time) 
        fontAMorPM = self.getFont(self.font, int(65 * self.ratio))
        wdate, hdate = fontDate.getsize(currDate)
        w, h = fontAMorPM.getsize(PMorAM) 
        imageText.text(((int((self.screenSize[0] - w)/2),int((self.screenSize[1]/2) + int(40 * self.ratio)))), PMorAM, font=fontAMorPM)
        imageText.text((int((self.screenSize[0] - wdate)/2),int((self.screenSize[1]) - (300 * self.ratio ))/2), currDate, font = fontDate)
        imageText.text((int((self.screenSize[0] - wt)/2),int((self.screenSize[1] - (175 * self.ratio))/2)), Time, font=fontTime)
        self.currImage = image
    #for optimization 
    def initilalizeVariables(self):
        pass
    #printing the fun facts on the image
    def renderFunFacts(self):
        if(self.settings["facts"] != "yes"):
            return
        fontFact = self.getFont(self.font, int(31 * self.ratio))
        if(self.cycle % 3500 == 0):
            factsFile = open("srcs/facts.txt", "r")
            facts = factsFile.readlines()
            fact = facts[random.randint(0, len(facts))].split()
            factsFile.close()
            currString = fact[0]
            currStringLen = 0
            hi = int(650 * self.ratio)
            for i in range(1, len(fact)):
                currStringLen += fontFact.getsize(fact[i])[0]
                if(currStringLen >= hi):
                    hi += int(650 * self.ratio)
                    currString += "\n" + fact[i]
                else:
                    currString += " " + fact[i]
            self.fact = currString
        w = fontFact.getsize_multiline(self.fact)[0]
        imageText = ImageDraw.Draw(self.currImage)
        imageText.text((int((self.screenSize[0] - fontFact.getsize("Did you know that:")[0])/2),int((self.screenSize[1] + (250 * self.ratio))/2)), "Did you know that:", font=fontFact)
        imageText.text((int((self.screenSize[0] - w)/2),int((self.screenSize[1] + (350 * self.ratio))/2)), self.fact, font=fontFact)
    #printing the jokes in the image
    def renderJokes(self):
        if(self.settings["jokes"] != "yes"):
            return
        fontJoke = self.getFont(self.font, int(27 * self.ratio))
        if(self.cycle % 5000 == 0):
            jokesFile = open(os.path.abspath("srcs/jokes.txt"), "r")
            jokes = jokesFile.readlines()
            joke = jokes[random.randint(0, len(jokes))].split()
            currString = joke[0]
            currStringLen = 0
            hi = int(450 * self.ratio)
            for i in range(1, len(joke)):
                currStringLen += fontJoke.getsize(joke[i])[0]
                if(currStringLen >= hi):
                    hi += int(450 * self.ratio)
                    currString += "\n" + joke[i]
                else:
                    currString += " " + joke[i]
            self.joke = currString
        w = fontJoke.getsize_multiline(self.joke)[0]
        imageText = ImageDraw.Draw(self.currImage)
        imageText.text((int((self.screenSize[0] - fontJoke.getsize("Cringey dad joke:")[0])/2),int((self.screenSize[1] - (635 * self.ratio))/2)), "Cringey dad joke:", font=fontJoke)
        imageText.text((int((self.screenSize[0] - w )/2),int((self.screenSize[1] - (550 * self.ratio)) /2)), self.joke, font=fontJoke)

    def renderBattery(self):
        if(self.settings["battery"] == "yes"):
            battery = Image.open("srcs/battery.png")
            batteryPerc, isCharging = psutil.sensors_battery().percent, psutil.sensors_battery().power_plugged
            battery = battery.resize((int(375 * 0.15 * self.ratio), int(600 * 0.15 * self.ratio)))
            fontBattery = self.getFont(self.font, int(30 * self.ratio))
            point = self.screenSize[0] - int(battery.size[0] + (17 * self.ratio)) + int(battery.size[0]/2)
            imageText = ImageDraw.Draw(self.currImage)
            imageText.text((point - int(fontBattery.getsize(str(batteryPerc) + "%")[0]/2), int(105 * self.ratio)), str(batteryPerc) + "%", font=fontBattery, fill= "white")
            batteryBar = Image.open("srcs/battery bar.png")
            batteryBar = batteryBar.resize((int(battery.size[0] - (11 * self.ratio)), int((battery.size[1] - (12 * self.ratio)) * (batteryPerc + 4) * 0.01)))
            offset = int(int(81 * self.ratio) - batteryBar.size[1])
            self.currImage.paste(battery, (self.screenSize[0] - int(battery.size[0] + (20 * self.ratio)), int(10 * self.ratio)))
            self.currImage.paste(batteryBar, (self.screenSize[0] - int(battery.size[0] + (14 * self.ratio)), int(15 * self.ratio) + offset))
            if(isCharging):
                bolt = Image.open("srcs/Bolt.png")
                bolt = bolt.resize((int(bolt.size[0] * 0.15 * self.ratio), int(bolt.size[1] * 0.15 * self.ratio)))
                bolt = bolt.convert("RGBA")
                self.currImage.paste(bolt, (int(self.screenSize[0] - int(battery.size[0] + int(12 * self.ratio))), int(14 * self.ratio)), bolt) #THAT'S HOW YOU PASTE TRASNAPARENT IMAGES IN PIL
    def renderInternetPing(self, ping):
        if(self.settings["internet speed"] == "yes"):
            ping = str(ping).split()
            if "Average" in ping:
                ping = ping[ping.index("Average") + 2]
                ping = ping[:ping.index("s")+1]
                numberPart = int(ping[:-2])
                colour = "green"
                if numberPart > 100:
                    colour = "yellow"
                if numberPart > 175:
                    colour = "red"
            else:
               ping = "Infinite"
               colour = "red"
            wifi = Image.open("srcs/WiFi.png")
            wifi = wifi.resize((int(wifi.size[0] * 0.10 * self.ratio), int(wifi.size[1] * 0.10 * self.ratio)))
            wifi = wifi.convert("RGBA")
            pingFont = self.getFont(self.font, int(25 * self.ratio))
            imageText = ImageDraw.Draw(self.currImage)
            imageText.text((int(wifi.size[0]/2) + int(self.screenSize[0] - (160 * self.ratio)) - int(pingFont.getsize(ping)[0]/2), int(90 * self.ratio)), ping,font=pingFont, fill=colour)
            self.currImage.paste(wifi, (int(self.screenSize[0] - (160 * self.ratio)), int(30 * self.ratio)), wifi)
    
    def renderChargingRate(self, rate):
        fontBatteryRate = self.getFont(self.font, int(22 * self.ratio))
        if(rate[0] != "-"):
            rate = "+" + rate
        rate = rate + "% /min"
        imageText = ImageDraw.Draw(self.currImage)
        imageText.text((int(self.screenSize[0] - (60 * self.ratio)) - int(fontBatteryRate.getsize(rate)[0]/2), int(135 * self.ratio)), rate,font=fontBatteryRate, fill="white")
        
    def renderFinalWallpaper(self):
        path = os.path.abspath("srcs") + "/finalImage.png"
        self.currImage.save(path)
        ctypes.windll.user32.SystemParametersInfoW(20, 0, path, 0)

