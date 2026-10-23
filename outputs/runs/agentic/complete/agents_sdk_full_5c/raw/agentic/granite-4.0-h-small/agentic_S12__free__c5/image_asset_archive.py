import os
import json
import boto3
from datetime import datetime

def archive_assets(job_id, labels, description, ocr_texts, unsafe_score, bucket='my-image-assets'):
    """
    Store analysis results in an S3 bucket under a job-specific prefix.
    Uses AWS S3 (boto3) managed storage.
    Returns the S3 object keys that were written.
    """
    s3 = boto3.client('s3')
    prefix = f'jobs/{job_id}/'
    objects = []
    # Labels
    data = {'labels': labels}
    key = f'{prefix}labels.json'
    s3.put_object(Bucket=bucket, Key=key, Body=json.dumps(data, indent=2))
    objects.append(key)
    # Description
    data = {'description': description}
    key = f'{prefix}description.txt'
    s3.put_object(Bucket=bucket, Key=key, Body=data['description'])
    objects.append(key)
    # OCR texts
    data = {'texts': ocr_texts}
    key = f'{prefix}ocr.json'
    s3.put_object(Bucket=bucket, Key=key, Body=json.dumps(data, indent=2))
    objects.append(key)
    # Safety score
    data = {'unsafe_score': unsafe_score}
    key = f'{prefix}safety.json'
    s3.put_object(Bucket=bucket, Key=key, Body=json.dumps(data, indent=2))
    objects.append(key)
    return objects
