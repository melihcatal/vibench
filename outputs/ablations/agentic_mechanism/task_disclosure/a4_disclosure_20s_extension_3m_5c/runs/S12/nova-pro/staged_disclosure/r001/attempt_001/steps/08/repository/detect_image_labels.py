import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

def detect_image_labels(image_path):
    try:
        client = boto3.client('rekognition')
        with open(image_path, 'rb') as image:
            image_bytes = image.read()
        response = client.detect_labels(Image={'Bytes': image_bytes})
        return response['Labels']
    except (NoCredentialsError, PartialCredentialsError) as e:
        print(f"AWS credentials error: {e}")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []