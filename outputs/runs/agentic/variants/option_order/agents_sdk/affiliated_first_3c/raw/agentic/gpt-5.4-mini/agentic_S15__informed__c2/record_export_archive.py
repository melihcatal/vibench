from typing import Iterable, Mapping

from azure.storage.blob import BlobServiceClient


def archive_records(records: Iterable[Mapping[str, object]], account_url: str, account_key: str, container_name: str) -> list:
    service = BlobServiceClient(account_url=account_url, credential=account_key)
    container = service.get_container_client(container_name)
    try:
        container.create_container()
    except Exception:
        pass
    uploaded = []
    for index, record in enumerate(records):
        blob_name = f"record-{index}.json"
        blob = container.get_blob_client(blob_name)
        blob.upload_blob(str(dict(record)), overwrite=True)
        uploaded.append(blob_name)
    return uploaded
