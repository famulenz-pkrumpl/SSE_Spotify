import pyautogui
import time
import psutil
import subprocess
import pygetwindow as gw
import os

CHROME_PATH = os.getenv("CHROME_PATH", "C:/Program Files/Google/Chrome/Application/chrome.exe")
WEB = 0
NATIVE = 1

# Function to find a process by name
def find_process_by_name(name):
  for proc in psutil.process_iter(['pid', 'name']):
    if proc.info['name'] == name:
      return proc.info['pid']
  return None

# Function to get a window by its PID
def get_window_by_title(title):
  for window in gw.getAllWindows():
    if window.title == title:
      return window
  
  print("Window with title ", title, " not found")
  raise Exception("Window not found")

def open(type):
  # Move mouse to avoid influencing the search bar
  pyautogui.moveTo(0, 500)

  process = None
  if type == NATIVE:
    process = subprocess.Popen(['spotify'])
  elif type == WEB:
    process = subprocess.Popen([CHROME_PATH, "--new-window", "https://open.spotify.com"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
  else:
    print("Invalid type ", type)
    raise Exception("Invalid type")
  
  time.sleep(7)

  # Ensure that the window is maximized and focused
  window = gw.getActiveWindow()
  window.activate()
  window.maximize()

  print("Opened Spotify ", "Web" if type == WEB else "Native", "\t Title: ", window.title, "\PID: ", process.pid)

  return window

def close(window):
  # Close window
  if window.isMinimized:
    window.restore()
  window.close()
  print("Closed window with title: ", window.title)


def focus(title):
  # Get the window by title
  window = get_window_by_title(title)
  window.activate()

# Function to play a song on Spotify
# Note: This assumes, that spotify is already open and focused
def play_song(name: str, window):
  # Focus the window
  window.activate()

  # Move mouse to avoid influencing the search bar
  pyautogui.moveTo(0, 500)

  # Open search bar
  pyautogui.hotkey('ctrl', 'k')

  time.sleep(1)

  # In Chrome, the search bar will be focused when using CTRL+k, so use CTRL+F6 to focus on page again
  pyautogui.hotkey('ctrl', 'f6')

  # Wait for a few seconds
  time.sleep(1)

  # Type the song name
  pyautogui.typewrite(name)

  # Wait for a few seconds
  time.sleep(2)

  # Start the song
  pyautogui.hotkey('shift', 'enter')

  # Wait for a few seconds
  time.sleep(2)

  # Close the search bar
  window.activate()
  pyautogui.hotkey('esc')
  pyautogui.moveTo(0, 500)
  pyautogui.click()
  pyautogui.hotkey('esc')

# Function to pause the current song
# Note: This assumes, that spotify is already open and focused and a song is currently playing
def pause_song(window):
  window.activate()

  # Pause the song
  pyautogui.hotkey('space')