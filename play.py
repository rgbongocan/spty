import argparse

from client import get_spotify_client


def resume(args):
    spfy = get_spotify_client()
    if not spfy.current_playback()["is_playing"]:
        spfy.start_playback()


def play_track(args):
    spfy = get_spotify_client()
    track = " ".join(args.track)
    res = spfy.search(track, limit=1)
    if items := res["tracks"]["items"]:
        spfy.start_playback(uris=[items[0]["uri"]])
    else:
        print("No matches found")


def play_album(args):
    spfy = get_spotify_client()
    album = " ".join(args.album)
    res = spfy.search(album, limit=1, type="album")
    if items := res["albums"]["items"]:
        spfy.start_playback(context_uri=items[0]["uri"])
    else:
        print("No matches found")


def play_list(args):
    spfy = get_spotify_client()
    playlist = " ".join(args.playlist)
    res = spfy.search(playlist, limit=1, type="playlist")
    if items := res["playlists"]["items"]:
        spfy.start_playback(context_uri=items[0]["uri"])
    else:
        print("No matches found")


def play_commands(parser):
    parser.set_defaults(func=resume)
    subparsers = parser.add_subparsers(dest="play_subsubparser")

    track_metavar = "track"
    track_parser = subparsers.add_parser(
        "track", usage=f"spotlite play track [-h] <{track_metavar}>"
    )
    track_parser.set_defaults(func=play_track)
    track_parser.add_argument(
        "track",
        default="",
        type=str,
        nargs=argparse.REMAINDER,
        metavar=track_metavar,
        help="Play a track",
    )

    album_parser = subparsers.add_parser(
        "album", usage="spotlite play album [-h] <album>"
    )
    album_parser.set_defaults(func=play_album)
    album_parser.add_argument(
        "album", default="", type=str, nargs="+", metavar="album", help="Play an album"
    )

    playlist_metavar = "playlist"
    playlist_parser = subparsers.add_parser(
        "list", usage=f"spotlite play list [-h] <{playlist_metavar}>"
    )
    playlist_parser.set_defaults(func=play_list)
    playlist_parser.add_argument(
        "playlist",
        default="",
        type=str,
        nargs="+",
        metavar=playlist_metavar,
        help="Play a playlist",
    )
