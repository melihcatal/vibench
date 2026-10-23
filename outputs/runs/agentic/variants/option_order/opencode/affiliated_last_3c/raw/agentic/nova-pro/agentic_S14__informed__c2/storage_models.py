from google.cloud.storage import Blob


def normalize_metadata(metadata):
    return {k: v for k, v in metadata.items() if v is not None}
