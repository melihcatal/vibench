import io
from database_client import get_s3_client

def record_export_archive(bucket_name: str, key: str, data: str | bytes) -> dict:
    """
    Archives exported document snapshots or attachments in AWS S3.
    Data can be a string or bytes.
    """
    s3 = get_s3_client()

    if isinstance(data, str):
        file_data = io.BytesIO(data.encode("utf-8"))
    else:
        file_data = io.BytesIO(data)

    response = s3.upload_fileobj(file_data, bucket_name, key)
    return response
