import pyautogui
import time
import psutil
import subprocess
import webbrowser
import pygetwindow as gw

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
  
  raise Exception("Window with title ", title, " not found")

# Function to open Spotify app and return the PID of the process
def open_native():
  # Open Spotify app
  process = subprocess.Popen(['spotify'])

  time.sleep(2)

  # Get the title of the current window
  native_window = gw.getActiveWindow()
  window_title = native_window.title
  print(f"Native window title: {window_title}")

  # Ensure that the window is maximized and focused
  window = get_window_by_title(window_title)
  window.activate()
  window.maximize()

  return window_title

def open_web():
  # Open the chrome browser and navigate to Spotify in a new window
  webbrowser.open_new('https://open.spotify.com')

  time.sleep(2)

  # Get the title of the current window
  web_window = gw.getActiveWindow()
  window_title = web_window.title
  print(f"Web window title: {window_title}")

  # Ensure that the window is maximized and focused
  window = get_window_by_title(window_title)
  window.activate()
  window.maximize()

  return window_title

def focus(title):
  # Get the window by title
  window = get_window_by_title(title)
  print("Focusing window with title: ", window.title)
  print("Window: ", window)
  window.activate()

# Function to play a song on Spotify
# Note: This assumes, that spotify is already open and focused
def play_song(name: str):
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
  time.sleep(1)

  # Close the search bar
  pyautogui.hotkey('esc')

  print("Playing song: ", name)

# Function to pause the current song
# Note: This assumes, that spotify is already open and focused and a song is currently playing
def pause_song():
  # Pause the song
  pyautogui.hotkey('space')