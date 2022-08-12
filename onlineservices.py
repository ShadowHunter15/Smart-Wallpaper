import subprocess
from subprocess import PIPE
class SmartWallpaperOnlineServies():
    def getInternetPing(self):
        hostname = "www.google.com"
        response = subprocess.run("ping -n 1 " + hostname, stdout=PIPE, stderr=PIPE)
        return response
