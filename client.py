import spotipy
from spotipy import util

CLIENT_ID = "23503e502dd54c53a15e50d8f4bc9ecc"
CLIENT_SECRET = "b69d6ad88e334a52abd05dc688ebd906"
REDIRECT_URI = "http://localhost:9090/"
SCOPES = [
    "user-read-playback-state",
    "user-read-currently-playing",
    "user-modify-playback-state",
    "user-library-read",
]

username = "count_gbrl"

spfy = None


def get_spotify_client():
    global spfy
    if not spfy:
        token = util.prompt_for_user_token(
            username,
            scope=" ".join(SCOPES),
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            redirect_uri=REDIRECT_URI,
        )
        if token:
            spfy = spotipy.Spotify(auth=token)
        else:
            print("Can't get token for", username)
    return spfy
