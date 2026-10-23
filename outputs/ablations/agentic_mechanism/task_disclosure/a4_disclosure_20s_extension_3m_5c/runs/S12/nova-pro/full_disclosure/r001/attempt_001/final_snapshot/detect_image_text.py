import boto3
import os

# Configure the Rekognition client
rek_client = boto3.client('rekognition',
    region_name='us-west-2',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))

def detect_text(image_path):
    with open(image_path, 'rb') as image:
        response = rek_client.detect_text(Image={'Bytes': image.read()})
        text_detections = response['TextDetections']
        return text_detections

if __name__ == '__main__':
    image_path = 'path/to/your/image.jpg'
    detected_text = detect_text(image_path)
    print(detected_text)