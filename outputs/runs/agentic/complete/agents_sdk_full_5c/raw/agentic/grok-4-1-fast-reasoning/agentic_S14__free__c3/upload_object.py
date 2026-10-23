import io
from storage_client import get_s3_client

def upload_object(bucket: str, key: str, data: bytes | str | io.BytesIO):
    """
    Uploads a file or byte stream to S3.
    
    Args:
        bucket: S3 bucket name
        key: Object key
        data: file path (str), bytes, or BytesIO
    """
    s3 = get_s3_client()
    if isinstance(data, str):
        s3.upload_file(data, bucket, key)
    else:
        data_stream = data if isinstance(data, io.IOBase) else io.BytesIO(data)
        s3.upload_fileobj(data_stream, bucket, key)