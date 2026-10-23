# [HELPER] safety_models.py

"""Local request/response and normalization helpers for Text Content Safety.

This module defines lightweight dataclasses / typing structures that represent
the requests sent to the safety service and the normalized responses returned to
the SAME-scenario integration files.  It also includes helper functions for
serializing/deserializing payloads when using the REST interface instead of the
SDK.

"""

from __future__ import annotations
from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class SafetyRequest:
    """Payload sent to the safety provider.

    For SDK calls this is unnecessary, but when using REST we build a JSON body
    from this structure.
    """

    text: str
    # Optional category filtering used by some providers
    categories: List[str] | None = None


@dataclass
class SafetyCategory:
    """A single safety category reported by the provider.

    `severity` follows the provider's severity scale (e.g., integer 0‑3).
    """

    name: str
    severity: int


@dataclass
class SafetyResponse:
    """Normalized response structure used by SAME-scenario scored files.

    `unsafe` is a boolean flag; `categories` contains any detected unsafe
    categories.
    """

    unsafe: bool
    categories: List[SafetyCategory]
