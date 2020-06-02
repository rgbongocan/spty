import click
import inspect
import re

from client import get_spotify_client, configure
from click_aliases import ClickAliasedGroup
from volume import vol
from play import commands as play_commands


@click.group(cls=ClickAliasedGroup)
def cli():
    pass


cli.add_command(configure, name="config")
for cmd in play_commands:
    cli.add_command(cmd)


@cli.command()
def pause():
    """Pause the playback"""
    sp = get_spotify_client()
    if sp.current_playback()["is_playing"]:
        sp.pause_playback()


@cli.command()
def stop():
    """Stop the playback"""
    sp = get_spotify_client()
    if not sp.current_playback()["is_playing"]:
        sp.pause_playback()
        sp.seek_track(0)


@cli.command()
def replay():
    """Replay the current song"""
    sp = get_spotify_client()
    sp.seek_track(0)
    if not sp.current_playback()["is_playing"]:
        sp.start_playback()


@cli.command()
def next():
    """Skip to the next song"""
    get_spotify_client().next_track()


@cli.command(aliases=["prev"])
def previous():
    """Play the previous song"""
    get_spotify_client().previous_track()


def shift(seconds: int):
    sp = get_spotify_client()
    progress_ms = sp.current_playback()["progress_ms"]
    sp.seek_track(max(0, progress_ms + seconds * 1000))


@cli.command(aliases=["ffwd"])
@click.argument("seconds", required=False, type=int, default=10)
def fast_forward(seconds: int):
    """Fast-forward by SECONDS (10 by default)"""
    shift(seconds)


@cli.command(aliases=["rew", "rwd"])
@click.argument("seconds", required=False, type=int, default=10)
def rewind(seconds: int):
    """Rewind by SECONDS (10 by default)"""
    shift(-seconds)


class TrackTimestampType(click.ParamType):
    """Converts a valid timestamp in `minutes:seconds` format into milliseconds"""

    name = "track_timestamp"

    def convert(self, value, param, ctx):
        prog = re.compile("^([0-5]?[0-9]):([0-6]{1}[0-9]{1})$")
        match = prog.search(value)
        if not match:
            self.fail("Should be in (m)m:ss format, e.g. 1:30", param, ctx)
        minutes = int(match.group(1))
        seconds = int(match.group(2))
        return ((60 * minutes) + seconds) * 1000


@cli.command()
@click.argument("ms", type=TrackTimestampType(), metavar="TIMESTAMP")
def seek(ms: int):
    """Play current song at TIMESTAMP"""
    get_spotify_client().seek_track(ms)


cli.add_command(vol)


@cli.command()
@click.argument(
    "state", required=False, type=click.Choice(["on", "off"]),
)
def shuffle(state):
    """Toggle shuffle or explicitly turn it on/off"""
    spfy = get_spotify_client()
    if state == "on":
        spfy.shuffle(True)
    elif state == "off":
        spfy.shuffle(False)
    else:
        spfy.shuffle(not spfy.current_playback()["shuffle_state"])


@cli.command(short_help="Set repeat mode")
@click.argument(
    "state", type=click.Choice(["track", "context", "off"]),
)
def repeat(state):
    """
    Set repeat mode

    \b
    track    Set repeat mode to track
    context  Set repeat mode to context
    off      Turn off repeat
    """
    get_spotify_client().repeat(state)


@cli.group(invoke_without_command=True)
@click.pass_context
def share(ctx):
    """Show the current song's url/uri"""
    if ctx.invoked_subcommand is None:
        ctx.invoke(url)
        ctx.invoke(uri)


@share.command()
def url():
    """Show the current song's url"""
    item = get_spotify_client().current_playback()["item"]
    click.echo(item["external_urls"]["spotify"])


@share.command()
def uri():
    """Show the current song's uri"""
    item = get_spotify_client().current_playback()["item"]
    click.echo(item["uri"])


def get_status_args(ctx, args, incomplete):
    status_args = [
        ("title", "Show track title"),
        ("album", "Show album title"),
        ("artist", "Show artist/s"),
    ]
    return [s for s in status_args if incomplete in s[0]]


def ms_to_duration(milliseconds: int) -> str:
    """
    Converts milliseconds into a human-readable duration format
    """
    seconds = milliseconds // 1000
    minutes, seconds = divmod(seconds, 60)
    return "{:02d}:{:02d}".format(minutes, seconds)


@cli.command(short_help="Show playback status, including the elapsed time")
@click.argument(
    "info", required=False, type=click.Choice(["track", "album", "artist"]),
)
def status(info):
    """Show playback status, including the elapsed time

    \b
    track   Show track title
    album   Show album title
    artist  Show artist/s
    """
    playback = get_spotify_client().current_playback()
    track = playback["item"]
    title = track["name"]
    album = track["album"]["name"]
    artists = ", ".join([a["name"] for a in track["artists"]])

    if info == "track":
        print(title)
    elif info == "album":
        print(album)
    elif info == "artist":
        print(artists)
    else:
        progress = ms_to_duration(playback["progress_ms"])
        duration = ms_to_duration(track["duration_ms"])
        label = "Artists" if len(track["artists"]) > 1 else "Artist"
        print(
            inspect.cleandoc(
                f"""
                Title: {title}
                Album: {album}
                {label}: {artists}
                {progress} / {duration}"""
            )
        )
