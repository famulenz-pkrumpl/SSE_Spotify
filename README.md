# 🌳 Sustainable Software Engineering - Spotify 🎧

## Introduction

This repository contains a script designed to measure and compare the energy consumption of both the Spotify Web Player and the Spotify Desktop App. The experiment involves playing the same set of songs in a randomized order on both platforms while recording their energy consumption.

A detailed discussion on the findings of this experiment is available [here](https://luiscruz.github.io/course_sustainableSE/2025/p1_measuring_software/g25_spotify.html).

## Requirements

Ensure you have the following dependencies installed:

- EnergyBridge (Setup guide can be found [here](https://github.com/tdurieux/energibridge))
- Python 3.8+
- Chrome webbrowser
- Spotify Desktop App
- Required Python libraries (listed in requirements.txt)

To install the required python libraries, the following command can be used:
```bash
pip install -r requirements.txt
```

## Preparation

Before starting the experiment, make sure that all the following points are fulfilled:

- The device should run for at least 1 hour before the experiment starts
- The battery of the device should be full and the device should be plugged in
- All other applications except for the console executing the Python script should be closed
- Close/Disable all unnecessary background services (e.g. Google Drive Synchronization, Software Updaters, ...)
- Turn off all notifications
- Make sure that no additional hardware is plugged into the device (e.g. remove USB mouse)
- The device must have a working internet connection (preferably a cable connection)
- Switch off auto brightness
- Disable all enegry saving modes of your device
- Need to be already logged in on Spotify Web and Desktop application
  - **Attention**: Since Spotify synchronizes the song that is currently played throughout different devices and apps, you need to have to distinct and working Spotify accounts for both Web and Desktop.
- Ensure that the volume in both spotify Web and Desktop is 100%
- The script will open the default browser, so Chrome should be set as default browser
- Make sure that the room temperature stay roughly the same during the experiment

## Experiment Methodology

For a more detailed explanation of how the experiment is conducted, please refer to the [article](https://luiscruz.github.io/course_sustainableSE/2025/p1_measuring_software/g25_spotify.html).

## Execution

Before executing the script, please copy the `.env` file and adjust your seetings.

```bash
cp .env.example .env
```

The experiment including the warm up can be started by executing the `main.py` file.

```bash
py main.py
```