import os

def normalize_upload_params(bucket, key, file_path=None, byte_stream=None):
    """Normalizes upload parameters for S3 client calls.
    Ensure exactly one source is provided.
    """
    if file_path and byte_stream:
        raise ValueError('Provide either file_path or byte_stream, not both.')
    return {
        'Bucket': bucket,
        'Key': key,
        'File': file_path,
        'Body': byte_stream
    }

def normalize_download_params(bucket, key):
    """Normalizes parameters for presigned download URL generation.
    """
    return {
        'Bucket': bucket,
        'Key': key
    }

def normalize_head_params(bucket, key):
    """Normalizes HEAD object parameters.
    """
    return {
        'Bucket': bucket,
        'Key': key
    }

def normalize_list_params(bucket, prefix='', delimiter='', max_keys=1000):
    """Normalizes list-objects parameters.
    """
    return {
        'Bucket': bucket,
        'Prefix': prefix,
        'Delimiter': delimiter,
        'MaxKeys': max_keys
    }
