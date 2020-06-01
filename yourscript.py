# import os
import click
import re

from client import get_spotify_client
from click_aliases import ClickAliasedGroup


@click.group(cls=ClickAliasedGroup)
def cli():
    pass


@cli.command()
def next():
    get_spotify_client().next_track()


@cli.command(aliases=["prev"])
def previous():
    get_spotify_client().previous_track()


@cli.command()
def play():
    sp = get_spotify_client()
    if not sp.current_playback()["is_playing"]:
        sp.start_playback()


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


@cli.command()
def stop():
    """Stop playback"""
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


class VolumeGroup(click.Group):
    def parse_args(self, ctx, args):
        parsed_args = super(VolumeGroup, self).parse_args(ctx, args)
        if ctx.params["v"] in {"up", "down"}:
            v, ctx.params["v"] = ctx.params["v"], None
            ctx.protected_args.append(v)
        return parsed_args


@cli.group(invoke_without_command=True, cls=VolumeGroup)
@click.argument("v", nargs=1, required=False)
@click.pass_context
def vol(ctx, v):
    if ctx.invoked_subcommand is None:
        if v:
            cmd = set
            ctx.params["perc"] = int(ctx.params.pop("v"))
        else:
            del ctx.params["v"]
            cmd = show
        ctx.forward(cmd)


@vol.command()
@click.argument("perc", type=int)
def set(perc: int):
    """Set volume to PERC"""
    get_spotify_client().volume(perc)


@vol.command()
def show():
    """Show current volume"""
    sp = get_spotify_client()
    click.echo(sp.current_playback()["device"]["volume_percent"])


@vol.command()
def up():
    click.echo("Volume up")


@vol.command()
def down():
    click.echo("Volume down")


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
@click.argument("ms", required=True, type=TrackTimestampType(), metavar="TIMESTAMP")
def seek(ms: int):
    """Play current song at TIMESTAMP"""
    get_spotify_client().seek_track(ms)


@cli.command()
def pause():
    sp = get_spotify_client()
    if sp.current_playback()["is_playing"]:
        sp.pause_playback()
