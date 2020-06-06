import click
import hashlib
import ruamel.yaml
import spotipy

from pathlib import Path
from spotipy import util

config = {}
CONFIG_FILE_PATH = f"{Path.home()}/spty.yaml"
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
    with open(CONFIG_FILE_PATH, "a+") as fp:
        fp.seek(0)
        config = yaml.load(fp) or {"redirect_uri": "http://localhost:9090/"}
    # placing outside of write block so the og config
    # is preserved in case the user aborts the prompt
    new_config = {
        key: click.prompt(text, default=config.get(key), type=str).strip()
        for key, text in [
            ("username", "Spotify username"),
            ("client_id", "Client ID"),
            ("client_secret", "Client Secret"),
            ("redirect_uri", "Redirect URI"),
        ]
    }
    with open(CONFIG_FILE_PATH, "w+") as fp:
        yaml.dump(new_config, fp)
    return new_config


@click.command(name="config")
def configure_command():
    """Configure your spotify app values"""
    prompt_config()


def configure():
    global config
    with open(CONFIG_FILE_PATH, "a+") as fp:
        fp.seek(0)
        _config = yaml.load(fp) or {}
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
        scopes = " ".join(SCOPES)
        scope_hash = hashlib.sha1(scopes.encode("utf-8")).hexdigest()
        token = util.prompt_for_user_token(
            username,
            scope=" ".join(SCOPES),
            client_id=config["client_id"],
            client_secret=config["client_secret"],
            redirect_uri=config["redirect_uri"],
            cache_path=f"{Path.home()}/.cache-{username}-{scope_hash[:16]}",
        )
        if token:
            sp = spotipy.Spotify(auth=token)
        else:
            click.echo("Can't get token for", username)
            return None
    return sp
