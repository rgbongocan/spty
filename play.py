import click

from config import get_spotify_client
from services import generate_autocompletion


class PlayGroup(click.Group):
    def parse_args(self, ctx, args):
        parsed_args = super(PlayGroup, self).parse_args(ctx, args)
        q = ctx.params["query"]
        if q and q[0] in {"album", "artist", "list"}:
            ctx.protected_args.append(q[0])
            ctx.args.append(" ".join(q[1:]))
        else:
            ctx.params["query"] = " ".join(q)
        return parsed_args


@click.group(cls=PlayGroup, invoke_without_command=True)
@click.argument(
    "query",
    nargs=-1,
    type=str,
    required=False,
    autocompletion=generate_autocompletion(
        [
            ("album", "Find an album and play it"),
            ("artist", "Find an artist and play their discography"),
            ("list", "Find a playlist and play it"),
        ]
    ),
)
@click.pass_context
def play(ctx, query: str):
    """
    Play a track, album, artist, or playlist
    \f
    p is the same as ctx["p"]
    """
    if not ctx.invoked_subcommand:
        ctx.forward(play_track)


@play.command(name="track")
@click.argument("query", required=False, type=str)
def play_track(query: str):
    """Find a track and play it / resume playback"""
    sp = get_spotify_client()
    if query:
        res = sp.search(query, limit=1)
        items = res["tracks"]["items"]
        if items:
            sp.start_playback(uris=[items[0]["uri"]])
        else:
            click.echo("No matches found")
    elif not sp.current_playback()["is_playing"]:
        sp.start_playback()


@play.command(name="album")
@click.argument("query", type=str)
def play_album(query: str):
    """Find an album and play it"""
    sp = get_spotify_client()
    res = sp.search(query, limit=1, type="album")
    items = res["albums"]["items"]
    if items:
        sp.start_playback(context_uri=items[0]["uri"])
    else:
        click.echo("No matches found")


@play.command(name="artist")
@click.argument("query", nargs=-1, type=str)
def play_discography(query: str):
    """Find an artist and play their discography"""
    sp = get_spotify_client()
    res = sp.search(query, limit=1, type="artist")
    items = res["artists"]["items"]
    if items:
        sp.start_playback(context_uri=items[0]["uri"])
    else:
        click.echo("No matches found")


@play.command(name="list")
@click.argument("query", nargs=-1, type=str)
def play_list(query: str):
    """Find a playlist and play it"""
    sp = get_spotify_client()
    res = sp.search(query, limit=1, type="playlist")
    items = res["playlists"]["items"]
    if items:
        sp.start_playback(context_uri=items[0]["uri"])
    else:
        click.echo("No matches found")
