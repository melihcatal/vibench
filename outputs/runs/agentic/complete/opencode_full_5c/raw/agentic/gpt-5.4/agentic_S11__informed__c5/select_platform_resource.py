from __future__ import annotations

from model_client import resolve_chat_resource


def select_platform_resource() -> dict[str, str]:
    resource = resolve_chat_resource()
    return {
        "provider": resource["provider"],
        "deployment": resource["deployment"],
        "resource_id": resource["resource_id"],
    }
