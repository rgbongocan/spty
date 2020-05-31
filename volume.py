from client import get_spotify_client


def increase_volume(args):
    spfy = get_spotify_client()
    current = spfy.current_playback()["device"]["volume_percent"]
    if current == 100:
        print("Already at max volume")
    else:
        to = min(current + 10, 100)
        spfy.volume(to)
        print(f"Volume increased to {to}")


def decrease_volume(args):
    spfy = get_spotify_client()
    current = spfy.current_playback()["device"]["volume_percent"]
    if current == 0:
        print("Already muted")
    else:
        to = max(0, current - 10)
        spfy.volume(to)
        print(f"Volume decreased to {to}")


def set_volume(args):
    spfy = get_spotify_client()
    spfy.volume(args.percentage)


def show_volume(args):
    spfy = get_spotify_client()
    current = spfy.current_playback()["device"]["volume_percent"]
    print(current)


def volume_commands(parser):
    parser.set_defaults(func=show_volume)
    subparsers = parser.add_subparsers(dest="volume_subsubparser")
    subparsers.add_parser("up", help="Increase volume by 10").set_defaults(
        func=increase_volume
    )
    subparsers.add_parser("down", help="Decrease volume by 10").set_defaults(
        func=decrease_volume
    )
    set_parser = subparsers.add_parser("set", help="Set volume to specified value")
    set_parser.set_defaults(func=set_volume)
    set_parser.add_argument(
        "percentage", type=int, nargs="?", help="Set volume from 0 to 100"
    )
