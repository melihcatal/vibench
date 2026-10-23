import datetime
from storage_client import get_gcs_client, get_bucket_name
from storage_models import PresignedUrlResponse

def generate_download_signed_url_v4(blob_name: str):
    """
    Generates a v4 signed URL for downloading a blob.

    Note: This uses the V4 signing process, which is recommended for GCS.
    The service account needs the "Service Account Token Creator" IAM role.
    
    Args:
        blob_name (str): The name of the object in the bucket.

    Returns:
        A PresignedUrlResponse containing the URL and its expiration.
    """
    client = get_gcs_client()
    bucket_name = get_bucket_name()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    expiration_time = datetime.timedelta(hours=1)
    
    url = blob.generate_signed_url(
        version="v4",
        expiration=expiration_time,
        method="GET",
    )
    
    expiration_datetime = datetime.datetime.now(datetime.timezone.utc) + expiration_time

    return PresignedUrlResponse(
        object_name=blob_name,
        url=url,
        expiration=expiration_datetime
    )
