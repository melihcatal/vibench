from pathlib import Path
from typing import Union, Dict, Optional, Any
from storage_client import get_s3_client

def upload_object(
    bucket: str,
    object_key: str,
    data: Union[bytes, str, Path],
    content_type: Optional[str] = None,
    metadata: Optional[Dict[str, str]] = None
) -> str:
    """
    Uploads a file or byte stream to Amazon S3.
    Returns the ETag.
    """
    client = get_s3_client()
    if isinstance(data, (str, Path)):
        with open(data, 'rb') as f:
            body = f.read()
    else:
        body = data
    kwargs: Dict[str, Any] = {
        'Bucket': bucket,
        'Key': object_key,
        'Body': body
    }
    if content_type:
        kwargs['ContentType'] = content_type
    if metadata:
        kwargs['Metadata'] = metadata
    response = client.put_object(**kwargs)
    return response['ETag']