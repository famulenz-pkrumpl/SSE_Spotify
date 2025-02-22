import os
import time

import record
import spotify
import screen_brightness_control as sbc

from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
from dotenv import load_dotenv

load_dotenv()

VOLUME = float(os.getenv("VOLUME", 0.2))
BRIGHTNESS = int(os.getenv("BRIGHTNESS", 50))


# Handles for spotify web a native windows
spotify_web = None
spotify_native = None


def unmute_and_set_volume(level):
  devices = AudioUtilities.GetSpeakers()
  interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
  volume = interface.QueryInterface(IAudioEndpointVolume)

  if volume.GetMute():
    volume.SetMute(0, None)

  volume.SetMasterVolumeLevelScalar(level, None)


def set_brightness(level):
  sbc.set_brightness(level)


# Initialize the experiment
def init():
  # TODO: maybe adapt any energy settings for the PC automatically

  # Set volume and brightness of the system
  unmute_and_set_volume(VOLUME)
  set_brightness(BRIGHTNESS)

  # Open Spotify native
  global spotify_native
  spotify_native = spotify.open_native()
  time.sleep(5)

  # Open Spotify web
  global spotify_web
  spotify_web = spotify.open_web()
  time.sleep(5)

  # TODO: initialize EnergiBridge  # Create monitoring service
  record.setup_service()

# Simple implementation of the fibonacci sequence used for warm up
def fibonacci(n):
  if n <= 1:
    return n
  else:
    return fibonacci(n-1) + fibonacci(n-2)

# Do some warm up before actually running the experiment
# The warm up is done by running a CPU intensive task (fibonacci)
def warm_up():
  print("Start warm up")
  # Warm up for 1 minute
  warm_up_time = 60
  start_time = time.time()

  i = 1
  while time.time() - start_time < warm_up_time:
    print(fibonacci(i), " ")
    i = i + 1

  print("Warm up completed")
  time.sleep(1)

  return


# Run the experiment
def run_experiment():
  # TODO: implement experiment run

  songs = [
    "Never Gonna Give You Up",
    "Take On Me"
  ]

  for i, song in enumerate(songs):
    output_file_name = f"experiment_{i}.csv"

    print(f"Running experiment for song: {song}")
    process = record.run_energibridge(output_file_name, 20)

    # Focus the native Spotify app
    spotify.focus(spotify_native)
    time.sleep(1)
    spotify.play_song(song)
    time.sleep(10)
    spotify.pause_song()
    time.sleep(1)

    process.wait()
  
  return


# Start the procedure
#warm_up()
init()
run_experiment()

