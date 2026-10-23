from __future__ import annotations

from typing import Dict

from security_client import build_secret_reference, get_secret_manager_client



def read_secret_version(secret_id: str, version: str = "latest") -> Dict[str, str]:
    client = get_secret_manager_client()
    ref = build_secret_reference(secret_id=secret_id, version=version)
    response = client.access_secret_version(request={"name": ref.resource_name()})
    metadata = client.get_secret_version(request={"name": ref.resource_name()})
    return {
        "provider": "Google Cloud Secret Manager",
        "name": ref.resource_name(),
        "state": metadata.state.name,
        "etag": metadata.etag,
        "payload": response.payload.data.decode("utf-8"),
    }
