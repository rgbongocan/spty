import click
from client import get_spotify_client


class VolumeGroup(click.Group):
    def parse_args(self, ctx, args):
        parsed_args = super(VolumeGroup, self).parse_args(ctx, args)
        if ctx.params["v"] in {"up", "down"}:
            v, ctx.params["v"] = ctx.params["v"], None
            ctx.protected_args.append(v)
        return parsed_args


def get_vol_args(ctx, args, incomplete):
    vol_args = [("up", "Increase volume"), ("down", "Decrease volume")]
    return [v for v in vol_args if incomplete in v[0]]


@click.group(invoke_without_command=True, cls=VolumeGroup)
@click.argument("v", nargs=1, required=False, autocompletion=get_vol_args)
@click.pass_context
def vol(ctx, v):
    """Show / adjust volume"""
    if ctx.invoked_subcommand is None:
        if v:
            cmd = set_volume
            ctx.params["perc"] = int(ctx.params.pop("v"))
        else:
            del ctx.params["v"]
            cmd = show_volume
        ctx.forward(cmd)


@vol.command(name="set")
@click.argument("perc", type=int)
def set_volume(perc: int):
    """Set volume to PERC"""
    get_spotify_client().volume(perc)


@vol.command(name="show")
def show_volume():
    """Show current volume"""
    sp = get_spotify_client()
    click.echo(sp.current_playback()["device"]["volume_percent"])


@vol.command(name="up")
def increase_volume():
    """Increase volume by 10"""
    spfy = get_spotify_client()
    current = spfy.current_playback()["device"]["volume_percent"]
    if current == 100:
        click.echo("Already at max volume")
    else:
        to = min(current + 10, 100)
        spfy.volume(to)
        click.echo(f"Volume increased to {to}")


@vol.command(name="down")
def decrease_volume():
    """Decrease volume by 10"""
    spfy = get_spotify_client()
    current = spfy.current_playback()["device"]["volume_percent"]
    if current == 0:
        click.echo("Already muted")
    else:
        to = max(0, current - 10)
        spfy.volume(to)
        click.echo(f"Volume decreased to {to}")
