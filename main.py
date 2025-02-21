import time
import spotify

# Open Spotify app
spotify_native = spotify.open_native()
time.sleep(5)

# Open Spotify web
spotify_web = spotify.open_web()
time.sleep(5)

# Focus the native Spotify app
spotify.focus(spotify_native)
time.sleep(1)
spotify.play_song("Shape of You")
time.sleep(10)
spotify.pause_song()
time.sleep(1)

# Focus the web Spotify app
spotify.focus(spotify_web)
time.sleep(1)
spotify.play_song("Never gonna give you up", True)
time.sleep(10)
spotify.pause_song()
time.sleep(1)