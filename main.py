import ctypes
from configuration import SmartWallpaperConfiguration
from offlineservices import SmartWallpaperOfflineServices
from renderer import SmartWallpaperRenderer
from onlineservices import SmartWallpaperOnlineServies
import time
settings, screenSize = SmartWallpaperConfiguration().configuration, SmartWallpaperConfiguration().ScreenSize
Sw = SmartWallpaperRenderer(settings, screenSize)

while True:
    try:
        time.sleep(2)
        Sw.mainLoop()
    except OSError:
        print("error")
        ctypes.windll.user32.SystemParametersInfoW(20, 0, r"C:\Users\osdrw\Desktop\Programming\Python\Smart wallpaper\srcs\finalImage.png", 0)

    