from __future__ import annotations

from collections import defaultdict
from typing import Any, Callable, Hashable, Iterable


def groupby(iterable: Iterable, keyfunc: Callable) -> dict[Hashable, list[Any]]:
    """Group iterable by key function. The items are grouped by the value that
    is returned by the `keyfunc`

    Parameters
    ----------
    iterable : list, tuple or iterable
        List of items to group
    keyfunc : callable
        Used to determine the group of each item. These become the keys
        of the returned dictionary

    Returns
    -------
    grouped : dict
        Returns a dictionary with the grouped values.
    """
    grouped = defaultdict(list)
    for item in iterable:
        key = keyfunc(item)
        grouped[key].append(item)

    return grouped
