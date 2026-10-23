import os
import boto3
from datetime import datetime

def image_asset_archive(image_path, analysis_result):
    """Archives image and its visual analysis results to Amazon S3.
    Creates a folder structure like s3://my-bucket/YYYYMMDD/image_id/
    and stores three objects:
      - original image
      - label JSON
      - safety flag JSON
    Returns the S3 URI of the folder.
    """
    s3 = boto3.client('s3')
    # Simple bucket & prefix configuration (could be externalized)
    bucket = os.getenv('AWS_S3_BUCKET', 'my-static-image-assets')
    date_prefix = datetime.utcnow().strftime('%Y%m%d')
    unique_id = os.path.splitext(os.path.basename(image_path))[0]
    prefix = f'{date_prefix}/{unique_id}/'
    # Upload original image (as bytes)
    with open(image_path, 'rb') as f:
        s3.upload_fileobj(f, bucket, prefix + 'image.jpg')
    # Upload label analysis JSON
    s3.put_object(Bucket=bucket, Key=prefix + 'labels.json', Body=json.dumps(analysis_result['labels']).encode())
    # Upload safety flag JSON
    s3.put_object(Bucket=bucket, Key=prefix + 'safety.json', Body=json.dumps({'safe': analysis_result['safe']}).encode())
    return f's3://{bucket}/{prefix}'
