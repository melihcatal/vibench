import datetime
from storage_client import get_storage_client


def create_presigned_download_url(
    bucket_name: str, object_name: str, expiration_minutes: int = 60
):
    """
    Generates a presigned URL to download an object from Google Cloud Storage.

    :param bucket_name: The name of the GCS bucket.
    :param object_name: The name of the object.
    :param expiration_minutes: The number of minutes the URL should be valid for.
    :return: A presigned URL string.
    """
    storage_client = get_storage_client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(object_name)

    expiration = datetime.timedelta(minutes=expiration_minutes)

    url = blob.generate_signed_url(
        version="v4",
        expiration=expiration,
        method="GET",
    )
    return url
