import click
from client import get_spotify_client


@click.command()
@click.argument("track", nargs=-1, required=False, type=str)
def play(track):
    """Find a track and play it / resume playback"""
    track = " ".join(track)
    spfy = get_spotify_client()
    if track:
        spfy = get_spotify_client()
        res = spfy.search(track, limit=1)
        items = res["tracks"]["items"]
        if items:
            spfy.start_playback(uris=[items[0]["uri"]])
        else:
            click.echo("No matches found")
    elif not spfy.current_playback()["is_playing"]:
        spfy.start_playback()


@click.command()
@click.argument("album", nargs=-1, type=str)
def album(album: str):
    """Find an album and play it"""
    spfy = get_spotify_client()
    album = " ".join(album)
    res = spfy.search(album, limit=1, type="album")
    items = res["albums"]["items"]
    if items:
        spfy.start_playback(context_uri=items[0]["uri"])
    else:
        click.echo("No matches found")


@click.command()
@click.argument("artist", nargs=-1, type=str)
def artist(artist: str):
    """Find an artist and play their discography"""
    spfy = get_spotify_client()
    artist = " ".join(artist)
    res = spfy.search(artist, limit=1, type="artist")
    items = res["artists"]["items"]
    if items:
        spfy.start_playback(context_uri=items[0]["uri"])
    else:
        click.echo("No matches found")


@click.command()
@click.argument("playlist", nargs=-1, type=str)
def playlist(playlist: str):
    """Find a playlist and play it"""
    spfy = get_spotify_client()
    playlist = " ".join(playlist)
    res = spfy.search(playlist, limit=1, type="playlist")
    items = res["playlists"]["items"]
    if items:
        spfy.start_playback(context_uri=items[0]["uri"])
    else:
        click.echo("No matches found")


commands = [play, album, artist, playlist]
