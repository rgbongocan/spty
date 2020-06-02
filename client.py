import click
import ruamel.yaml
import spotipy

from spotipy import util

config = {}
SCOPES = [
    "user-read-playback-state",
    "user-read-currently-playing",
    "user-modify-playback-state",
    "user-library-read",
]

sp = None
yaml = ruamel.yaml.YAML()


@click.command()
def configure():
    click.echo(
        "If you haven't yet, create your spotify app at https://developer.spotify.com/dashboard/"
    )
    config = {
        "username": click.prompt("Spotify username", type=str),
        "client_id": click.prompt("Client ID", type=str),
        "client_secret": click.prompt("Client Secret", type=str),
        "redirect_uri": click.prompt("Redirect URI", type=str),
    }
    with open("config.yaml", "w") as fp:
        yaml.dump(config, fp)


def get_spotify_client():
    global config, sp
    if not config:
        with open("config.yaml") as fp:
            config = yaml.load(fp)

    if not sp:
        username = config["username"]
        token = util.prompt_for_user_token(
            username,
            scope=" ".join(SCOPES),
            client_id=config["client_id"],
            client_secret=config["client_secret"],
            redirect_uri=config["redirect_uri"],
        )
        if token:
            sp = spotipy.Spotify(auth=token)
        else:
            click.echo("Can't get token for", username)
            return None
    return sp
