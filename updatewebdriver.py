import shutil
import json
import requests
import urllib.request
import os

from zipfile import ZipFile


class WebDriver:
    currentWebDriverVersion = None
    wantedWebDriverVersion = None
    jsonEndpoints = "https://googlechromelabs.github.io/chrome-for-testing/latest-patch-versions-per-build-with-downloads.json"
    downloadLink = None

    def __init__(self, errorMessage, folder):
        self.GetCurrentWebDriverVersion(errorMessage)
        self.GetWantedWebDriverVersion(errorMessage)
        self.GetDownloadLink(requests.get(self.jsonEndpoints))
        self.DownloadFileAndReplaceIt(folder)

    def GetCurrentWebDriverVersion(self, errorMessage):
        start_index = str(errorMessage).find("Chrome version ")
        if start_index != -1:
            self.currentWebDriverVersion = str(errorMessage)[start_index + len("Chrome version "):].split()[0]
            print(f"Chrome version: {self.currentWebDriverVersion}")
            return True
        else:
            print("Chrome version not found in the error message.")
            return False

    def GetWantedWebDriverVersion(self, errorMessage):
        start_index = str(errorMessage).find("Current browser version is ")
        if start_index != -1:
            self.wantedWebDriverVersion = str(errorMessage)[start_index + len("Current browser version is "):].split()[
                0]
            parts = self.wantedWebDriverVersion.split('.')
            self.wantedWebDriverVersion = '.'.join(parts[:-1])
            print(f"Browser version: {self.wantedWebDriverVersion}")
            return True
        else:
            print("Browser version not found in the error message.")
            return False

    def GetDownloadLink(self, request):
        response = json.loads(request.text)
        for key, value in response["builds"].items():
            if key == self.wantedWebDriverVersion:
                chromeDrivers = value["downloads"]["chromedriver"]
                for chromeDriver in chromeDrivers:
                    if chromeDriver["platform"] == "win32":
                        self.downloadLink = chromeDriver["url"]
                        return True
        return False

    def DownloadFileAndReplaceIt(self, folder):
        try:
            urllib.request.urlretrieve(self.downloadLink, folder + ".zip")
            shutil.rmtree(folder)
            with ZipFile(folder + ".zip", 'r') as zObject:
                zObject.extractall()
            os.remove(folder + ".zip")
        except:
            print('Error DownloadFileAndReplaceIt')

        return True
