from storage_client import get_storage_client
from storage_models import StorageObject


def upload_file_to_gcs(storage_object: StorageObject):
    """
    Uploads a file or byte stream to a Google Cloud Storage bucket.

    Args:
        storage_object: A StorageObject dataclass instance containing bucket,
                        key, and content.
    """
    client = get_storage_client()
    bucket = client.bucket(storage_object.bucket)
    blob = bucket.blob(storage_object.key)

    if storage_object.content is not None:
        blob.upload_from_string(storage_object.content)
    else:
        raise ValueError("Content must be provided for upload.")

    if storage_object.metadata:
        blob.metadata = storage_object.metadata
        blob.patch()

    return f"gs://{storage_object.bucket}/{storage_object.key}"
