# Discord Music Bot Project

## Overview

This project involves the creation of a Discord music bot capable of playing songs based on user commands. The bot receives song titles either directly from the server or receives a link to YouTube. It plays the requested songs on the Discord server and provides a set of commands for controlling playback and managing playlists.

## Functionality

### Music Playback
- **Command: -play "song name"**
  - Adds the specified song to the playlist queue.

- **Command: -pause**
  - Pauses the currently playing song.

- **Command: -resume**
  - Resumes playback after a pause.

- **Command: -stop**
  - Stops the entire playlist queue.

- **Command: -next**
  - Skips to the next song in the playlist queue.

- **Command: -delete "song number"**
  - Deletes a specific song from the playlist.

- **Command: -join**
  - Joins the server without playing any music.

- **Command: -leave**
  - Disconnects from the server and clears the playlist.

- **Command: -playlist**
  - Sends a message with the current playlist.

### Additional Commands
- **Command: -fox**
  - Sends a random fox image from the internet to the server chat.

- **Command: -online**
  - Sends a response to the server chat indicating that the bot is online.

## Implementation Details

The music bot is implemented using Discord API integration, and music playback is achieved through parsing YouTube or directly from server-provided links. The bot's commands allow users to manage the music playback, manipulate playlists, and enjoy additional features like random fox images.

## Conclusion

This Discord music bot project aims to provide an interactive and entertaining experience for users by enabling music playback and offering additional fun commands.

