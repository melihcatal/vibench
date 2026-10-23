import requests


def metrics_export_archive(payload, config=None):
    config = config or {}
    response = requests.put(config["archive_url"], headers={"Authorization": f"Bearer {config.get('archive_token', '')}"}, data=payload["content"], timeout=30)
    response.raise_for_status()
    return {"archived": True, "provider": "google-cloud-storage"}
