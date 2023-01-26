import subprocess
from subprocess import PIPE
class SmartWallpaperOnlineServies():
    def __init__(self) -> None:
        if "Average" in str(self.getInternetPing()):
            print("ONLINE SERVICES: GO")
        else:
            print("ONLINE SERVICES: FAIL")
    def getInternetPing(self):
            hostname = "www.google.com"
            response = subprocess.run("ping -n 1 " + hostname, stdout=PIPE, stderr=PIPE)
            return response
