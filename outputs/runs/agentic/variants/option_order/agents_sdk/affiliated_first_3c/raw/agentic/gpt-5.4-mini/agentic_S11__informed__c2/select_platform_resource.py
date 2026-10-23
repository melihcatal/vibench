from __future__ import annotations

from model_client import resolve_platform_resource
from model_models import PlatformSelection


def select_platform_resource(model_hint: str | None = None) -> PlatformSelection:
    return resolve_platform_resource(model_hint)
