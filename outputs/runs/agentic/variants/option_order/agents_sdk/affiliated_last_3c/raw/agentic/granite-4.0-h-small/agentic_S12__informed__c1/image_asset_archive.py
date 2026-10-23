import boto3
import hashlib
from datetime import datetime

# Amazon S3 client
s3 = boto3.client('s3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name='us-east-1')

def archive_analysis_to_s3(image_id, analysis_json, bucket='image-analysis-archive'):
    """Store analysis JSON as a versioned object in S3."""
    timestamp = datetime.utcnow().isoformat().replace(':', '-')
    key = f'{image_id}/{timestamp}.json'
    # Ensure bucket exists (simple check)
    s3.put_object(Bucket=bucket, Key=key, Body=json.dumps(analysis_json))
    return {'Bucket': bucket, 'Key': key}
