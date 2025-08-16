import keyboard
import subprocess
import requests
from RPLCD.i2c import CharLCD
import time

lcd = CharLCD(i2c_expander='PCF8574', address=0x27, port=1, cols=16, rows=2, dotsize=8)
lcd.clear()

buffer = ""
prevSearch = ""
viewerIP = "http://192.168.88.21:1337/"

# Define your commands based on keywords
commands = {
    "delete": "toggleScreenBlur",
    "insert": "toggleCamera",
    "right": "slideRight",
    "left": "slideLeft",
    "down": "scaleDown",
    "up": "scaleUp",
    "page up": "toggleMask",
    "+": "focus",
    "-": "toggleImage",
    "÷": "toggleBGVideo",
    "f3": "slot1",
    "f4": "slot2",
    "f5": "slot3",
    "f6": "slot4",
    "f7": "slot5",
    "f8": "lockBGImage",
    "f9": "toggleWhiteboard"
}

def handle_input(command):
    commandPath = commands[command]
    lcd.write_string(commandPath)
    res = requests.get(f"{viewerIP}{commandPath}")
    end_message(res.text)

def perform_search(query):
    res = requests.get(f"{viewerIP}search?query={query}")
    end_message(res.text)

def end_message(text):
    lcd.cursor_pos = (1, 0)
    lcd.write_string(text)

def on_key(event):
    global buffer
    global prevSearch
    key = event.name
    print(key)

    # Ignore keys without names or with more than one character (function keys, shift, etc.)
    if key is None or key == "unknown":
        return

    if key == "space" or key == "enter":
        if buffer and len(buffer) > 1:
            perform_search(buffer)
            prevSearch = buffer
            buffer = ""  # reset buffer
            return

    if key == "×":
        if prevSearch:
            perform_search(prevSearch)
            return

    lcd.clear()

    if key in commands:
        handle_input(key)
        buffer = ""
        return
    elif key == "backspace":
        buffer = buffer[:-1]
    elif len(key) == 1:  # only append single character keys
        buffer += key

    #lcd.cursor_pos = (0, 0)
    lcd.write_string(buffer)

keyboard.on_release(on_key)
print("Listening for input (terminate with Ctrl+C)...")
keyboard.wait()
