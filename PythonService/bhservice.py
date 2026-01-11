import os 
import servicemanager
import shutil
import subprocess
import sys

import win32event
import win32service
import win32serviceutil

SRCDIR='d:\\GitHub\\Black_Hat_Python\\PythonService'
TGTDIR='c:\\Windows\\temp'

class BHServerSvc(win32serviceutil.ServiceFramework):
    _svc_name_ = "BlackHatService"
    _svc_display_name_ = "Black Hat Service"
    _svc_description_ = ("Execute VBScripts at regular intervals. Not a malware :)")

    def __init__(self, args):
        self.vbs = os.path.join(TGTDIR, 'bhservice_task.vbs')
        self.timeout = 1000 * 60

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        self.ReportServiceStatus(win32service.SERVICE_RUNNING)
        self.main()


    def main(self):
        while True:
            ret_code = win32event.WaitForSingleObject(self.hWaitStop, self.timeout)
            if ret_code == win32event.WAIT_OBJECT_O:
                servicemanager.LogInfoMsg("Service is stopping")
                break
            src = os.path.join(SRCDIR, "bhservice_task.vbs")
            shutil.copy(src, self.vbs)
            subprocess.call(f"cscript.exe {self.vbs}", shell=False)

# script located at
# https://nostarch.com/black-hat-python2E

if __name__ == '__main__':
    if len(sys.argv) == 1:
        servicemanager.Inialize()
        servicemanager.PrepareToHostSingle(BHServerSvc)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(BHServerSvc)








