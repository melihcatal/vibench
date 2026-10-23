from __future__ import annotations

from translation_client import get_client


def unsafe_copy_check(text: str):
    client = get_client()
    return client.unsafe_copy_check(text)
