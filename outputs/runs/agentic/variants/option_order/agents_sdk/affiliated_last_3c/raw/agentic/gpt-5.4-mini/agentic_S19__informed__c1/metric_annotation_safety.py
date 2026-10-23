from __future__ import annotations

from observability_client import client


def metric_annotation_safety(text: str):
    return client().safety_check(text)
