import datetime
import subprocess
from datetime import datetime as dt
import winsound
import keyboard
class SmartWallpaperOfflineServices():
    def __init__(self):
        print("OFFLINE SERVICES: GO")
        self.Alarms = []
        self.times = set()
        self.ringtone = ""
        self.format = ""
        self.currDate = ""
        subprocess.run(r"srcs/BatteryInfoView.exe /stext srcs/battery.txt")
        self.Perc = ""
        file = open("srcs/text.txt").read()
        temp = file[file.index("%") + 48:file.index("%") + 55]
        for i in temp:
            if(i.isnumeric()):
                self.Perc += i
        self.Perc = int(self.Perc) / 10
    def getAlarms(self):
        with open("Alarms.txt","r") as f:
            for i in f.readlines():
                try:
                    i = i.replace(" ", "").lower()
                    midpoint = i.index(":")
                    hours = i[:midpoint]
                    twelve = 0 #uses 24 hour format
                    if("am" in i):
                        twelve = 1 # AM
                    elif ("pm" in i):
                        twelve = 2 #PM
                    minutes = i[midpoint+1:midpoint+3]
                    self.Alarms.append(list((hours, minutes, twelve)))
                except:
                    print("Error while reading alarms please make sure they are in the correct format.")
                self.parseAlarms()
    
    def getTime(self):
        if(self.format == "12"):
            Time = datetime.datetime.now().time().strftime("%I:%M")
        elif(self.format == "24"):
            Time = datetime.datetime.now().time().strftime("%H:%M")
        if(self.currDate != dt.today().strftime('%d-%m-%Y')):
            self.currDate = dt.today().strftime('%d-%m-%Y')

        return (Time, self.currDate)
    
    def parseAlarms(self):
            times = set()
            for i in self.Alarms:
                if(i[2] == 0):
                    times.add((i[0], i[1]))
                elif(i[2] == 1):
                    if(int(i[0]) == 12):
                        times.add(("00", i[1]))
                    else:
                        times.add((i[0], i[1]))
                else:
                    if(int(i[0]) == 12):
                        times.add((i[0], i[1]))
                    else:
                        times.add((str(int(i[0])+12), i[1]))
            self.times = times

    def checkAlarms(self):
        Time = datetime.datetime.now().time().strftime("%H:%M")
        currTime = (Time[:Time.index(":")], Time[Time.index(":")+ 1:])
        if(currTime in self.times):
            self.times.remove(currTime)
            self.ringAlarm()
    
    def getChargingRate(self):
        subprocess.run(r"srcs/BatteryInfoView.exe /stext srcs/battery.txt")
        batteryAmmount = ""
        file = open("srcs/battery.txt").read()
        for i in file[file.index("%") + 48:file.index("%") + 55]:
            if i.isnumeric():
                batteryAmmount += i;
        rate = int(batteryAmmount) / 10 - self.Perc
        self.Perc = int(batteryAmmount) / 10
        return str(round(rate * 1.55, 2))

    def ringAlarm(self):
        winsound.PlaySound(self.ringtone, winsound.SND_ASYNC + winsound.SND_LOOP)
    