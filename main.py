import ctypes
from configuration import SmartWallpaperConfiguration
from offlineservices import SmartWallpaperOfflineServices
from renderer import SmartWallpaperRenderer
from onlineservices import SmartWallpaperOnlineServies
import time
settings, screenSize = SmartWallpaperConfiguration().configuration, SmartWallpaperConfiguration().ScreenSize
Sw = SmartWallpaperRenderer(settings, screenSize)
online = SmartWallpaperOnlineServies()
errors = 0
while True:
    try:
        Sw.mainLoop()
        Sw.renderInternetPing(online.getInternetPing())
        Sw.renderFinalWallpaper()
        print("Cycle: " + str(Sw.cycle) + " || errors so far: "  + str(errors), end = '\r')
        time.sleep(3)
        
    except OSError as error: 
        errors += 1
        print("error: " + str(error))
        ctypes.windll.user32.SystemParametersInfoW(20, 0, r"C:\Users\osdrw\Desktop\Programming\Python\Smart wallpaper\srcs\finalImage.png", 0)

    
