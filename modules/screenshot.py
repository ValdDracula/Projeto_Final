import win32gui, pythoncom, pyWinhook, pyautogui, threading, autoit
from autoit import properties

def windowEnumerationHandler(hwnd, top_windows):
    top_windows.append((hwnd, win32gui.GetWindowText(hwnd)))

def disableInput():
    hm = pyWinhook.HookManager()
    hm.MouseAll = disable
    hm.KeyAll = disable
    hm.HookMouse()
    hm.HookKeyboard()


def enableInput():
    hm = pyWinhook.HookManager()
    hm.MouseAll = enable
    hm.KeyAll = enable
    hm.HookMouse()
    hm.HookKeyboard()

def disable(event):
    return False

def enable(event):
    return False

def screenshotAutopsy():
    thread = threading.Timer(2, screenshotAutopsy)
    thread.start()
    results = []
    top_windows = []
    win32gui.EnumWindows(windowEnumerationHandler, top_windows)
    for i in top_windows:
        if "autopsy" in i[1].lower():
            disableInput()
            autoit.win_activate(i[1])
            autoit.win_set_state(i[1], flag=properties.SW_SHOW)
            win32gui.SetForegroundWindow(i[0])
            pyautogui.screenshot('screenshot.png')
            enableInput()
            break
    thread.join()
if __name__ == "__main__":
    screenshotAutopsy()