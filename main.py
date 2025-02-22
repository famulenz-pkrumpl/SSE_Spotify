import time
import spotify
import random

# Constants
WEB = 0
NATIVE = 1

# Handles for spotify web an native windows
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

# Initialize the experiment
def init():
  # TODO: maybe adapt any energy settings for the PC automatically

  print("Start initialization")

  # Open Spotify native
  global spotify_native
  spotify_native = spotify.open_native()
  time.sleep(3)

  # Open Spotify web
  global spotify_web
  spotify_web = spotify.open_web()
  time.sleep(3)

  print("Initialization completed")

  # TODO: initialize EnergiBridge

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
  # Variables to adapt the experiment
  plays_per_song = 3          # Number of times each song is played
  song_play_duration = 60     # The duration a song is played in seconds
  pause_after_song = 60       # The pause between two songs in seconds

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
  # The songs and the active player are shuffeled randomly
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

    # TODO: start EnergiBridge for experiment i and active_player

    # Play the selected song
    spotify.focus(get_player(active_player))
    time.sleep(1)
    spotify.play_song(selected_song)
    time.sleep(song_play_duration)
    spotify.pause_song()
    time.sleep(1)

    # TODO: Stop EnergiBridge
    print("Starting pause ...")
    # TODO: Start EnerguBridge pause measurement

    # Pause
    time.sleep(pause_after_song)

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

