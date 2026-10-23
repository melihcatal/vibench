import os
import base64
import boto3
from vision_models import ImageInput, LabelDetectionResult

def detect_image_labels(image_input: ImageInput) -> LabelDetectionResult:
    client = boto3.client(
        'rekognition',
        region_name=os.environ.get('AWS_REGION', 'us-east-1'),
        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY')
    )

    if image_input.content_base64:
        image_bytes = base64.b64decode(image_input.content_base64)
        image_param = {'Bytes': image_bytes}
    elif image_input.image_uri:
        # Assuming image_uri is an S3 URI for direct Rekognition processing
        # Example: s3://your-bucket-name/path/to/image.jpg
        uri_parts = image_input.image_uri.replace('s3://', '').split('/', 1)
        if len(uri_parts) < 2:
            raise ValueError("S3 image_uri must be in format s3://bucket-name/object-key")
        bucket_name = uri_parts[0]
        object_key = uri_parts[1]
        image_param = {'S3Object': {'Bucket': bucket_name, 'Name': object_key}}
    else:
        raise ValueError("ImageInput must contain either content_base64 or image_uri")

    response = client.detect_labels(
        Image=image_param,
        MaxLabels=10,
        MinConfidence=75
    )

    labels = [
        {'name': label['Name'], 'confidence': label['Confidence']}
        for label in response['Labels']
    ]
    return LabelDetectionResult(labels=labels)