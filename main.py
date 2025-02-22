import time
import spotify

# Hndles for spotify web an native windows
spotify_web = None
spotify_native = None

# Initialize the experiment
def init():
  # TODO: maybe adapt any energy settings for the PC automatically

  # Open Spotify native
  global spotify_native
  spotify_native = spotify.open_native()
  time.sleep(5)

  # Open Spotify web
  global spotify_web
  spotify_web = spotify.open_web()
  time.sleep(5)

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
  # TODO: implement experiment run
  # Focus the native Spotify app
  spotify.focus(spotify_native)
  time.sleep(1)
  spotify.play_song("Never gonna give you up")
  time.sleep(10)
  spotify.pause_song()
  time.sleep(1)
  
  return


# Start the procedure
warm_up()
init()
run_experiment()

