import os
import json
import boto3
from botocore.exceptions import NoCredentialsError

def archive_analysis(analysis_summary, bucket_name, prefix='image_analysis/'):
    '''Upload analysis JSON to Amazon S3 as an archived artifact.
    analysis_summary: dict or JSON string produced by image_summary
    bucket_name: destination bucket name
    prefix: folder prefix inside bucket
    '''
    s3 = boto3.client('s3')
    try:
        # Ensure JSON string
        if isinstance(analysis_summary, dict):
            payload = json.dumps(analysis_summary, indent=2)
        else:
            payload = analysis_summary
        key = os.path.join(prefix, f'analysis_{os.urandom(4).hex()}.json')
        s3.put_object(Bucket=bucket_name, Key=key, Body=payload.encode('utf-8'))
        return {'bucket': bucket_name, 'key': key}
    except NoCredentialsError:
        raise RuntimeError('AWS credentials not available')
