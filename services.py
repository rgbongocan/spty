from typing import Callable, List, Tuple


def generate_autocompletion(args: List[Tuple[str, str]]) -> Callable:
    def get_args(ctx, args: List[Tuple[str, str]], incomplete) -> List[Tuple[str, str]]:
        return [a for a in args if incomplete in a[0]]

    return get_args
