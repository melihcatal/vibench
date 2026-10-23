# image_asset_archive.py
# [LATER-STEP] Archive image-analysis artifacts (labels, caption, OCR, safety) and derived captions in IBM Cloud Object Storage

import json
import os
from pathlib import Path
import boto3  # using boto3 here to demonstrate generic S3-like storage; you could use ibm-cos-sdk as well

# ----------------------------------------------------------------------------------------------
# Configuration (read from environment; you would set these before running)
# ----------------------------------------------------------------------------------------------
BUCKET_NAME = os.getenv('ARCHIVE_BUCKET', 'my-vision-assets')
REGION = os.getenv('AWS_REGION', 'us-east-1')
ENDPOINT_URL = os.getenv('AWS_ENDPOINT_URL')  # optional, for IBM Cloud Object Storage or other S3‑compatible services

# ----------------------------------------------------------------------------------------------
# Initialise a generic S3 client (boto3 works for S3 and most S3‑compatible services)
# ----------------------------------------------------------------------------------------------
s3 = boto3.client(
    's3',
    region_name=REGION,
    endpoint_url=ENDPOINT_URL,
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
)

# ----------------------------------------------------------------------------------------------
# Helper to store a JSON payload under a given key
# ----------------------------------------------------------------------------------------------
def store_json(key: str, payload: dict):
    s3.put_object(Bucket=BUCKET_NAME, Key=key, Body=json.dumps(payload), ContentType='application/json')

# ----------------------------------------------------------------------------------------------
# Archive a structured summary (produced by image_summary.py)
# ----------------------------------------------------------------------------------------------
def archive_summary(summary: dict):
    prefix = 'vision-analysis/'
    store_json(f'{prefix}labels.json', summary['labels'])
    store_json(f'{prefix}caption.txt', {'caption': summary['caption']})
    store_json(f'{prefix}ocr.json', summary['ocr_text'])
    store_json(f'{prefix}safety.txt', {'safety': summary['safety']})

# ----------------------------------------------------------------------------------------------
# Example CLI (uncomment to test directly)
# ----------------------------------------------------------------------------------------------
# if __name__ == '__main__':
#     import argparse
#     parser = argparse.ArgumentParser(description='Archive vision analysis results to object storage.')
#     parser.add_argument('summary_json', type=str, help='Path to JSON file containing the summary.')
#     args = parser.parse_args()
#     summary = json.load(open(args.summary_json, 'r', encoding='utf-8'))
#     archive_summary(summary)
#     print(f'Archived to bucket {BUCKET_NAME} with prefix vision-analysis/')

# ----------------------------------------------------------------------------------------------
# Note: This helper uses boto3 (Amazon S3 SDK) but can be pointed at IBM Cloud Object Storage,
# Google Cloud Storage, Azure Blob, etc., by adjusting the client configuration. It stores
# JSON representations of each artifact for downstream consumption.
# ----------------------------------------------------------------------------------------------
