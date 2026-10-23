from observability_client import ObservabilityClient


def metrics_export_archive(snapshot_name: str, content: dict):
    client = ObservabilityClient(endpoint="https://storage.azure.com")
    return client.post(f"/archive/{snapshot_name}", {"content": content, "service": "azure-blob-storage"})
