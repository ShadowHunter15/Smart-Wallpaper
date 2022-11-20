import ctypes
from PIL import Image
import os
class SmartWallpaperConfiguration():

    """
         creates a dictionary (self.configuration) with 
         the settings for the wallpaper
    """
    
    def __init__(self) -> None:
        print("CONFIGURATION: GO")
        self.configuration = {}
        user32 = ctypes.windll.user32
        user32.SetProcessDPIAware()
        self.ScreenSize = (user32.GetSystemMetrics(0), user32.GetSystemMetrics(1))
        self.config = self.load_config()
        self.parse_config(self.config)

    def load_config(self) -> list:
        with open("config.txt", "r") as f:
            f = list(map(lambda x: x[x.index(":")+1:].strip(), f.read().split("\n")))
            return f

    def parse_config(self, config) -> None:
        
        #region: wallpaper
        choice = None
        Wp = ""
        #user didn't choose a wallpaper, default will be used
        if config[0].lower() == "none":
            Wp = os.path.abspath("srcs/WP.jpg")
            choice = "default"
            
        # user choose a solid color  OR user provided a path to a wallpaper   
        elif config[0].lower() in "black, red, grey, white, green, yellow, blue, orange, purple":
            Wp = config[0]
            choice = "color"
        
        elif os.path.exists(config[0]):
            Wp = config[0]
            choice = "path"
        
        else:
            raise ValueError("Wallpaper choice can't be parsed")
        self.load_wallpaper(Wp, choice)
        #endregion
        
        #region: text font
        self.load_font(config[2])
        #endregion               

        #region: clock format
        if config[1] in ("24", "12"):
            self.configuration["clock format"] = config[1]
        else:
            raise ValueError("invalid choice for setting: clock format")
        #endregion
        
        #region: app usage, battery, alarms, reminders, weather, internet speed, news, crypto prices
        self.load_others(config)
        #endregion
    
    def load_wallpaper(self, wp, choice) -> None:
        #loading the wallpaper to the default fallback image or to a sepcified image
        if choice == "default" or choice == "path":
            self.configuration["wallpaper"] = Image.open(wp)

        #loading the wallpaper to the specified color
        elif choice == "color":
            img = Image.new("RGB", self.ScreenSize, color=wp)
            self.configuration["wallpaper"] = img

    def load_font(self, font) -> None:
        if font.lower() == "none":
            font = os.path.abspath("srcs/flower3.TTF")
        elif os.path.exists(font):
            font = os.path.abspath(font)
        else:
            raise ValueError("Font file couldn't be parsed")
        self.configuration["font"] = font     

    def load_others(self, config) -> None:
        configs = ["battery", "alarms", "reminders", "weather", "app usage", "internet speed", "news", "crypto", "facts", "jokes", "email", "cycle"]
        curr = 0
        for i in config[3:]:
            if i.lower() in ("yes", "no"):
                self.configuration[configs[curr]] = i
            else:
                raise ValueError("invalid choice for setting: " + configs[curr])
            curr +=1
