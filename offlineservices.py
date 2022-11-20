class SmartWallpaperOfflineServices():
    def __init__(self):
        print("OFFLINE SERVICES: GO")
        self.Alarms = []
        self.getAlarms()
    def getAlarms(self):
        Alarms = []
        with open("srcs/Alarms.txt","r") as f:
            for i in f.readlines():
                i = i.strip().lower()
                hours = i[:i.index(":")]
                
                if("am" in i or "pm" in i):
                    twelve = True
                    if("am" in i):
                        AM = True
                    else:
                        AM = False
                        
                else:
                    twelve = False
                
