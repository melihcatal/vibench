from __future__ import annotations

from typing import Optional

from model_client import resolve_vertex_resource
from model_models import PlatformResource


def select_platform_resource(model_name: Optional[str] = None) -> PlatformResource:
    return resolve_vertex_resource(model_name=model_name)
