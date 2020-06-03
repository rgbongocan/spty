# spty
A simple Spotify CLI using Click and Spotipy

This was made for personal use and as an exercise in making CLIs. However it should work fairly well, behaving similar to macOS `shpotify`. Tested on Ubuntu/Elementary and Zsh for now!

This does not communicate with your Spotify app directly but rather over API calls. It's a remote controller. As such, users need to have a Spotify premium account and create a Spotify app at https://developer.spotify.com/dashboard/. See https://developer.spotify.com/documentation/general/guides/app-settings/ for more instructions.

I'm working to make this available via pip. After cloning or installing, user will have to append the following to their `.zshrc` file to enable autocomplete:
```
"$(_SPTY_COMPLETE=source_zsh spty)"
````

Usage
```
spty                      On first use, will prompt user to configure their Spotify app values
spty config               Re/configure your Spotify app values

spty play                 Play or resume playback
spty play TRACK           Find a track and play it
spty play album ALBUM     Find an album and play it
spty play artist ARTIST   Find an artist and play its discography
spty play list PLAYLIST   Find a playlist and play it

spty pause                Pause the playback
spty stop                 Stop the playback
spty replay               Replay the current song
spty next                 Skip to the next song
spty previous (prev)      Play the previous song

spty fast-forward (ffwd)  Fast-forward by SECONDS (10 by default)
spty rewind (rew)         Rewind by SECONDS (10 by default)
spty seek                 Play current song at TIMESTAMP (e.g. 1:30)

spty vol                  Show current volume
spty vol up               Increase volume by 10
spty vol down             Decrease volume by 10
spty vol PERC             Set volume to PERC (0-100)
spty repeat               Set repeat mode (track, context, or off)
spty shuffle              Toggle shuffle or explicitly turn it on/off

spty status               Show playback status, including the elapsed time
spty status track         Show track title
spty status title         Show album title
spty status artist        Show artist/s

spty share                Show the current song's url and uri
stpy share url            Show the current song's url
stpy share uri            Show the current song's uri
```
