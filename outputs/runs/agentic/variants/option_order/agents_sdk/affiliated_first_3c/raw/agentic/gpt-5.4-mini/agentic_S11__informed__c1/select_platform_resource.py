from __future__ import annotations

from model_client import select_resource


def resolve(model_identifier: str) -> str:
    return select_resource(model_identifier)
