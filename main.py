import os
import time

import random
import record
import spotify
import screen_brightness_control as sbc

from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
from dotenv import load_dotenv

load_dotenv()

VOLUME = float(os.getenv("VOLUME", 0.2))
BRIGHTNESS = int(os.getenv("BRIGHTNESS", 50))

# Constants
WEB = 0
NATIVE = 1

# Handles for spotify web a native windows
spotify_web = None
spotify_native = None
def get_player(player):
  if player == WEB:
    return spotify_web
  elif player == NATIVE:
    return spotify_native
  else:
    print("Unknown player ", player)
    raise Exception("Unknown player")


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
  print("Start initialization")

  # Set volume and brightness of the system
  unmute_and_set_volume(VOLUME)
  set_brightness(BRIGHTNESS)

  # Open Spotify native
  global spotify_native
  spotify_native = spotify.open_native()
  time.sleep(3)

  # Open Spotify web
  global spotify_web
  spotify_web = spotify.open_web()
  time.sleep(3)

  # Create monitoring service
  record.setup_service()

  print("Initialization completed")


# Simple implementation of the fibonacci sequence used for warm up
def fibonacci(n):
  if n <= 1:
    return n
  else:
    return fibonacci(n-1) + fibonacci(n-2)

# Do some warm up before actually running the experiment
# The warm-up is done by running a CPU intensive task (fibonacci)
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
  # Variables to adapt the experiment
  plays_per_song = 1          # Number of times each song is played
  song_play_duration = 5     # The duration a song is played in seconds
  pause_after_song = 5       # The pause between two songs in seconds
  energibridge_duration = song_play_duration + 2  # Extra time because of sleeps

  experiment_start_time = time.time()
  time.sleep(1)

  # List of songs to play
  songs = [
    "Never gonna give you up",
    "Darude Sandstorm",
    "Summer of 69",
    "Dancing Queen",
    "Dont stop me now",
    "Im still standing",
    "Take on me",
    "Lose yourself",
    "Its my life",
    "Toto Africa"
  ]

  # Keep track of the plays of the songs in web and native
  plays = {
    WEB: [0] * len(songs),
    NATIVE: [0] * len(songs)
  }

  # Run the experiment
  # The songs and the active player are shuffled randomly
  for i in range(len(songs) * plays_per_song * 2):
    print("Starting experiment num #", str(i+1))

    # Randomly select a song and player
    selected_song = None
    while selected_song is None:
      # Randomly select the active player
      active_player = random.choice([WEB, NATIVE])

      # Randomly select a song
      song = random.choice(songs)
      song_index = songs.index(song)

      # Check if the song can be played
      if plays[active_player][song_index] < plays_per_song:
        selected_song = song
        plays[active_player][song_index] += 1
        print("Active player: ", get_player(active_player))
        print("Playing song: ", selected_song)
        print("New play count: ", plays[active_player][song_index])

    # Starting energibridge for the experiment
    output_file_name = f"experiment_{i+1}_{"web" if active_player == WEB else "native"}.csv"
    process = record.run_energibridge(output_file_name, energibridge_duration)

    print(active_player)
    if (active_player == WEB):
      print("web")

    # Play the selected song
    spotify.focus(get_player(active_player))
    time.sleep(1)
    spotify.play_song(selected_song)
    time.sleep(song_play_duration)
    spotify.pause_song()
    time.sleep(1)

    # Wait for energibridge experiment
    process.wait()

    print("Starting pause ...")

    # Starting energibridge for the pause
    output_file_name = f"pause_{i+1}.csv"
    process = record.run_energibridge(output_file_name, pause_after_song)

    # Pause
    time.sleep(pause_after_song)

    # Wait for energibridge pause
    process.wait()

    print("Experiment #", str(i+1), " completed\n")

  experiment_duration = time.time() - experiment_start_time
  print("===============================================")
  print("Experiment completed in ", experiment_duration, " seconds")
  print("Plays: ", plays)
  print("===============================================")

  return


# Start the procedure
warm_up()
init()
run_experiment()

