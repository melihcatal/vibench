from __future__ import annotations

from typing import Iterable, List

from model_client import HostedModelClient


EMBED_MODEL = "text-embedding-3-small"


def embed_outputs(texts: Iterable[str]) -> List[List[float]]:
    client = HostedModelClient()
    return client.embed(texts, model=EMBED_MODEL)
