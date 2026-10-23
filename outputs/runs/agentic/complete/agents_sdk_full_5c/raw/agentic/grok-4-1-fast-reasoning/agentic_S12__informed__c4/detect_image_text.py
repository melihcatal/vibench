import argparse
import boto3
import json
from vision_client import image_to_bytes
from vision_models import ImageText

def detect_image_text(image_path: str) -> ImageText:
    rekognition = boto3.client('rekognition', region_name=os.environ.get('AWS_REGION', 'us-east-1'))
    response = rekognition.detect_text(Image={'Bytes': image_to_bytes(image_path)})
    texts = [detection['DetectedText'] for detection in response['TextDetections']]
    return {'texts': texts}

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Detect text in image using Amazon Rekognition')
    parser.add_argument('image_path', help='Path to input image')
    args = parser.parse_args()
    result = detect_image_text(args.image_path)
    print(json.dumps(result, indent=2))