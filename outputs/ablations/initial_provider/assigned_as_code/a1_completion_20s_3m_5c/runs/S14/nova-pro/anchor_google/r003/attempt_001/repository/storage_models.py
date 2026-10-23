from google.cloud.storage import Blob


def normalize_blob(blob: Blob):
    return {
        "name": blob.name,
        "size": blob.size,
        "content_type": blob.content_type,
        "updated": blob.updated,
    }