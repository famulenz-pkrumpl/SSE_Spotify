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

# Constants
VOLUME = float(os.getenv("VOLUME", 0.2))
BRIGHTNESS = int(os.getenv("BRIGHTNESS", 50))
WEB = 0
NATIVE = 1

def get_player_name(player):
  if player == WEB:
    return "Web"
  elif player == NATIVE:
    return "Native"
  else:
    return ""

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
  # Warm up for 5 minutes
  warm_up_time = 300
  start_time = time.time()

  i = 1
  while time.time() - start_time < warm_up_time:
    print(fibonacci(i), " ")
    i = i + 1

  print("Warm up completed")
  time.sleep(1)

  return
  
def shuffle_songs(songs):
  songs_list = list(songs)
  random.shuffle(songs_list)
  return songs_list

# Run the experiment
def run_experiment():
  # Variables to adapt the experiment
  num_runs = 30               # The number of experiments to conduct per player
  song_play_duration = 20     # The duration a song is played in seconds
  experiment_pause = 60       # The pause between two songs in seconds

  experiment_start_time = time.time()
  time.sleep(1)

  # List of songs to play
  songs = [
    "Im still standing",
    "Lose yourself",
    "Its my life",
    "Never gonna give you up",
  ]

  # Duration of the measurement of EnergiBridge
  energibridge_duration = (song_play_duration + 6) * len(songs) # Extra time because of sleeps in spotify.play_song()

  # Create a random shuffle for the usage of the differnt players
  player_shuffle = [WEB, NATIVE] * num_runs
  random.shuffle(player_shuffle)

  # Run the experiment
  for i in range(num_runs * 2):
    print("Starting experiment num #", str(i+1))

    # Get the current active player from the randomly shuffled list
    active_player = player_shuffle[i]
    print("Active player: ", get_player_name(active_player))

    # Open the active player
    player_handle = spotify.open(active_player)

    # Starting energibridge for the experiment
    output_file_name = f"experiment_{i+1}_{'web' if active_player == WEB else 'native'}.csv"
    experiment_process = record.run_energibridge(output_file_name, energibridge_duration)

    # Shuffle the songs
    shuffled_songs = shuffle_songs(songs)

    # Play the songs on after another
    for song in shuffled_songs:
      # Play the song
      print("Playing song: ", song)
      spotify.play_song(song, player_handle)

      # Play the song for the defined duration
      time.sleep(song_play_duration)

    # Pause the song
    spotify.pause_song(player_handle)

    # Close the window
    spotify.close(player_handle)

    # Wait for energibridge experiment
    experiment_process.wait()

    print("Starting pause ...")

    # Starting energibridge for the pause
    output_file_name = f"pause_{i+1}.csv"
    pause_process = record.run_energibridge(output_file_name, experiment_pause)

    # Pause
    time.sleep(experiment_pause)

    # Wait for energibridge pause
    pause_process.wait()

    print("Experiment #", str(i+1), " completed\n")

  experiment_duration = time.time() - experiment_start_time
  print("===============================================")
  print("Experiment completed in ", experiment_duration, " seconds")
  print("Player execution order:", ["Web" if player == WEB else "Native" for player in player_shuffle])
  print("===============================================")

  return


# Start the procedure
warm_up()
init()
run_experiment()

