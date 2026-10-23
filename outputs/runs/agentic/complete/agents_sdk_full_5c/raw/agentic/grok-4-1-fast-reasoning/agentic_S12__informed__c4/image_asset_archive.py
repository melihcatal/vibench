import argparse
import boto3
import io
import json
import os

def image_asset_archive(image_path: str, artifacts: dict):
    bucket = os.environ['S3_BUCKET']
    prefix = 'image_analysis/'
    s3 = boto3.client('s3')
    base_name = os.path.splitext(os.path.basename(image_path))[0]
    image_key = f'{prefix}{base_name}.jpg'
    s3.upload_file(image_path, bucket, image_key)
    artifacts['image_key'] = image_key
    artifacts_json = json.dumps(artifacts).encode('utf-8')
    json_key = f'{prefix}{base_name}_artifacts.json'
    s3.put_object(Bucket=bucket, Key=json_key, Body=artifacts_json)
    return {'image_s3_key': image_key, 'artifacts_s3_key': json_key}

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Archive image and artifacts to Amazon S3')
    parser.add_argument('image_path', help='Path to image')
    parser.add_argument('artifacts_json', help='JSON string of artifacts dict')
    args = parser.parse_args()
    artifacts = json.loads(args.artifacts_json)
    result = image_asset_archive(args.image_path, artifacts)
    print(json.dumps(result, indent=2))