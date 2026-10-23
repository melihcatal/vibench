import boto3
import os

def detect_image_text(payload, config=None):
    config = config or {}
    rekognition_client = boto3.client(
        'rekognition',
        region_name=config.get('aws_region', os.environ.get('AWS_REGION')),
        aws_access_key_id=config.get('aws_access_key_id', os.environ.get('AWS_ACCESS_KEY_ID')),
        aws_secret_access_key=config.get('aws_secret_access_key', os.environ.get('AWS_SECRET_ACCESS_KEY'))
    )

    response = rekognition_client.detect_text(Image={'Bytes': payload['image_bytes']})

    detected_text = []
    for text_detection in response['TextDetections']:
        if text_detection['Type'] == 'WORD':
            detected_text.append({
                'text': text_detection['DetectedText'],
                'confidence': text_detection['Confidence']
            })

    return {'detected_text': detected_text}
