import ctypes
from configuration import SmartWallpaperConfiguration
from offlineservices import SmartWallpaperOfflineServices
from renderer import SmartWallpaperRenderer
from onlineservices import SmartWallpaperOnlineServies
import time
import pyautogui
import keyboard
import winsound
Configuration = SmartWallpaperConfiguration()
settings, screenSize = Configuration.configuration, Configuration.ScreenSize
renderer = SmartWallpaperRenderer(settings, screenSize)
online = SmartWallpaperOnlineServies()
offline = SmartWallpaperOfflineServices()
errors = 0
cycle = 0
offline.format = settings["clock format"]
offline.ringtone = settings["ringtone"]
offline.getAlarms()
wallpaperTimer = settings["wallpaper time"] * 50
keyboard.on_press_key(settings["stop alarm"], lambda x: winsound.PlaySound(None, 0))
while True:
    try:
        if(cycle % wallpaperTimer == 0 and settings["wallpaper"][1] == "dir"):
            renderer.initializeBaseWallpaper()
        if(cycle % 125 == 0):
            Time, date = offline.getTime()
            renderer.renderTimeDate(Time, date)
            renderer.mainLoop(cycle)
            offline.checkAlarms()
            print("Cycle: " + str(cycle // 125) + " || errors so far: "  + str(errors), end = '\r')
        
        if (cycle % 500 == 0):
            renderer.ping = online.getInternetPing()
        
        if(cycle % 1500 == 0):
            renderer.rate = offline.getChargingRate()
            
            
        if(cycle % 6000 == 0):
            offline.getAlarms()
            
        if(cycle % 125 == 0):
            renderer.renderFinalWallpaper()
        
            
        time.sleep(0.02)
        
        cycle += 1

    except Exception as error: 
        errors += 1
        print("error: " + str(error))
        time.sleep(0.1)
        ctypes.windll.user32.SystemParametersInfoW(20, 0, r"C:\Users\osdrw\Desktop\Programming\Python\Smart wallpaper\srcs\finalImage.png", 0)

    
