from typing import TypeVar, Iterable

_T = TypeVar('_T')


def join_till_limit(
        join: str,
        iterable: Iterable[str], *,
        prefix: str = "",
        postfix: str = "",
):
    message = prefix
    budget = 2000 - len(prefix) - len(postfix)
    is_first = True
    for elem in iterable:
        part = elem if is_first else (join + elem)
        is_first = False
        budget -= len(part)
        if budget < 0:
            break
        message += part
    return message + postfix
