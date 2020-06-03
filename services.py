from typing import Callable, List, Tuple


def generate_autocompletion(options: List[Tuple[str, str]]) -> Callable:
    def get_args(ctx, args: List[Tuple[str, str]], incomplete) -> List[Tuple[str, str]]:
        return [a for a in options if incomplete in a[0]]

    return get_args
