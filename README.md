# spty
A simple Spotify CLI using Click and Spotipy

This was made for personal use and as an exercise in making CLIs. However it should work fairly well, behaving similar to macOS `shpotify`. Tested on Ubuntu/Elementary and Zsh for now!

This does not communicate with your Spotify app directly but rather over API calls. It's a remote controller. As such, users need to have a Spotify premium account and create a Spotify app at https://developer.spotify.com/dashboard/. See https://developer.spotify.com/documentation/general/guides/app-settings/ for more instructions.

I'm working to make this available via pip. After cloning or installing, user will have to append the following to their `.zshrc` file to enable autocomplete:
```
"$(_SPTY_COMPLETE=source_zsh spty)"
````
