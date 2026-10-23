# [SAME-SCENARIO] moderate_batch.py

import os
from safety_client import TextSafetyClient


def moderate_messages(messages: list[str]) -> list[dict]:
    """Moderate a batch of user messages and return a list of per‑message decisions.

    The TextSafetyClient handles batching if supported by the underlying provider.
    Otherwise the function loops over messages individually.
    """
    client = TextSafetyClient()
    # If the provider supports true batch calls, pass the whole list; else map.
    if hasattr(client, "analyze_batch"):
        return client.analyze_batch(messages)
    return [client.analyze(msg) for msg in messages]
