import datetime
from storage_client import get_storage_client, get_bucket_name

def generate_download_signed_url_v4(object_name: str):
    """Generates a v4 signed URL for downloading a blob."""
    # bucket_name = "your-bucket-name"
    # object_name = "your-object-name"

    storage_client = get_storage_client()
    bucket_name = get_bucket_name()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(object_name)

    # V4 signing requires a service account key file.
    # You can specify the credentials file explicitly, or rely on
    # GOOGLE_APPLICATION_CREDENTIALS environment variable.
    url = blob.generate_signed_url(
        version="v4",
        # This URL is valid for 15 minutes
        expiration=datetime.timedelta(minutes=15),
        # Allow GET requests using this URL.
        method="GET",
    )

    print(f"Generated GET signed URL for {object_name}:")
    print(url)
    print("You can use this URL with any user agent, for example:")
    print(f"curl '{url}'")
    return url
