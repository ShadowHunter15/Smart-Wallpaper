import subprocess
from subprocess import PIPE
class SmartWallpaperOnlineServies():
    def __init__(self) -> None:
        if "Average" in str(self.getInternetPing(0)):
            print("ONLINE SERVICES: GO")
        else:
            print("ONLINE SERVICES: FAIL")
    def getInternetPing(self, cycle):
        if(cycle % 400) == 0:
            hostname = "www.google.com"
            response = subprocess.run("ping -n 1 " + hostname, stdout=PIPE, stderr=PIPE)
            return response
