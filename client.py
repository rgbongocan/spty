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


def prompt_config():
    click.echo("Acquire your config from https://developer.spotify.com/dashboard/")
    with open("config.yaml", "r") as fp:
        config = yaml.load(fp) or {}
    # placing outside of write block so the og config
    # is preserved in case the user aborts the prompt
    new_config = {
        key: click.prompt(text, default=config.get(key), type=str)
        for key, text in [
            ("username", "Spotify username"),
            ("client_id", "Client ID"),
            ("client_secret", "Client Secret"),
            ("redirect_uri", "Redirect URI"),
        ]
    }
    with open("config.yaml", "w") as fp:
        yaml.dump(new_config, fp)
    return new_config


@click.command()
def configure_command():
    """Configure your spotify app values"""
    prompt_config()


def configure():
    global config
    with open("config.yaml", "r") as fp:
        _config = yaml.load(fp)
        keys = {"username", "client_id", "client_secret", "redirect_uri"}
        misconfigured = not all(_config.get(k) for k in keys)
        if misconfigured:
            click.echo("Configure your spotify app properly first")
            config = prompt_config()
        else:
            config = _config


def get_spotify_client():
    global config, sp
    if not config:
        configure()
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
