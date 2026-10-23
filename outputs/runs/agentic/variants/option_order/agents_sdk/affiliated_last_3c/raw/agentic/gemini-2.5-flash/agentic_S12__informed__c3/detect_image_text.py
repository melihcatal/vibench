import os
import boto3

def detect_image_text(image_bytes: bytes):
    """Detects text appearing inside an image using Amazon Rekognition."""
    region = os.environ.get("AWS_REGION", "us-east-1")
    client = boto3.client("rekognition", region_name=region)

    response = client.detect_text(Image={'Bytes': image_bytes})
    
    text_detections = []
    for text in response['TextDetections']:
        if text['Type'] == 'WORD':
            text_detections.append(text['DetectedText'])
    return text_detections

if __name__ == '__main__':
    # This example requires AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY to be set.
    # For demonstration, load a local image or pass image bytes.
    # with open("path/to/your/image.jpg", "rb") as image_file:
    #     image_data = image_file.read()
    #     print(detect_image_text(image_data))
    pass
