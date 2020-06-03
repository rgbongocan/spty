import click

from config import get_spotify_client
from services import generate_autocompletion


class VolumeGroup(click.Group):
    def parse_args(self, ctx, args):
        parsed_args = super(VolumeGroup, self).parse_args(ctx, args)
        if ctx.params["v"] in {"up", "down"}:
            v, ctx.params["v"] = ctx.params["v"], None
            ctx.protected_args.append(v)
        return parsed_args


autocomplete_args = [
    ("up", "Increase volume"),
    ("down", "Decrease volume"),
]


@click.group(name="vol", cls=VolumeGroup, invoke_without_command=True)
@click.argument(
    "v",
    nargs=1,
    required=False,
    autocompletion=generate_autocompletion(autocomplete_args),
)
@click.pass_context
def volume(ctx, v):
    """Show / adjust volume"""
    if ctx.invoked_subcommand is None:
        if v:
            cmd = set_volume
            ctx.params["perc"] = int(ctx.params.pop("v"))
        else:
            del ctx.params["v"]
            cmd = show_volume
        ctx.forward(cmd)


@volume.command(name="set")
@click.argument("perc", type=int)
def set_volume(perc: int):
    """Set volume to PERC"""
    get_spotify_client().volume(perc)


@volume.command(name="show")
def show_volume():
    """Show current volume"""
    sp = get_spotify_client()
    click.echo(sp.current_playback()["device"]["volume_percent"])


@volume.command(name="up")
def increase_volume():
    """Increase volume by 10"""
    sp = get_spotify_client()
    current = sp.current_playback()["device"]["volume_percent"]
    if current == 100:
        click.echo("Already at max volume")
    else:
        to = min(current + 10, 100)
        sp.volume(to)
        click.echo(f"Volume increased to {to}")


@volume.command(name="down")
def decrease_volume():
    """Decrease volume by 10"""
    sp = get_spotify_client()
    current = sp.current_playback()["device"]["volume_percent"]
    if current == 0:
        click.echo("Already muted")
    else:
        to = max(0, current - 10)
        sp.volume(to)
        click.echo(f"Volume decreased to {to}")
