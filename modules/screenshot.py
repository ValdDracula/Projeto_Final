import ctypes
import pyautogui
import autoit

#Only Windows
GetWindowText = ctypes.windll.user32.GetWindowTextW
GetWindowTextLength = ctypes.windll.user32.GetWindowTextLengthW
IsWindowVisible = ctypes.windll.user32.IsWindowVisible
wantedWindow = None

def foreach_window(hwnd, lParam):
    if IsWindowVisible(hwnd):
        global wantedWindow
        length = GetWindowTextLength(hwnd)
        buff = ctypes.create_unicode_buffer(length + 1)
        GetWindowText(hwnd, buff, length + 1)
        if "autopsy" in str(buff.value).lower():
            wantedWindow = buff.value
    return True

def screenshotAutopsy():
    global wantedWindow
    print("----------------------HERE--------------------")
    EnumWindows = ctypes.windll.user32.EnumWindows
    EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))

    EnumWindows(EnumWindowsProc(foreach_window), 0)
    if wantedWindow is None:
        print("Plz notify admin that autopsy GUI is down")
    else:
        print("Im here")
        autoit.win_activate(wantedWindow)
        autoit.win_set_state(wantedWindow, flag=autoit.properties.SW_MAXIMIZE)
        pyautogui.screenshot("screenshot.png")
        autoit.win_set_state(wantedWindow, flag=autoit.properties.SW_MINIMIZE)



#if __name__ == "__main__":
#    screenshotAutopsy()