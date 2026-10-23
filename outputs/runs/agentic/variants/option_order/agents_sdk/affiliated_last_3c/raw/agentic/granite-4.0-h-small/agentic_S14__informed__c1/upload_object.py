import os
from storage_client import get_s3_client
from storage_models import normalize_upload_params

def upload_object(bucket, key, file_path=None, byte_stream=None):
    """Uploads a file or byte stream to Amazon S3.
    Uses boto3 S3 client obtained from storage_client.py.
    Exactly one of file_path or byte_stream must be provided.
    """
    if (file_path is None) == (byte_stream is None):
        raise ValueError('Provide exactly one of file_path or byte_stream')

    params = normalize_upload_params(bucket, key, file_path, byte_stream)
    s3 = get_s3_client()
    if file_path:
        s3.upload_file(params['Key'], params['Bucket'], params['File'])
    else:
        s3.put_object(Bucket=params['Bucket'], Key=params['Key'], Body=params['Body'])
    print(f'Uploaded {params["Key"]} to bucket {params["Bucket"]}')
