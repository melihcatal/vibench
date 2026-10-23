
import os
import boto3

def detect_image_text(image_bytes: bytes) -> list:
    """Detects text in an image using Amazon Rekognition."""
    client = boto3.client('rekognition', region_name=os.environ.get("AWS_REGION", "us-east-1"))
    
    response = client.detect_text(
        Image={'Bytes': image_bytes}
    )

    text_detections = []
    for text in response['TextDetections']:
        if text['Type'] == 'WORD':
            text_detections.append(text['DetectedText'])
    return text_detections

if __name__ == '__main__':
    # This is example usage.
    # Ensure AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY are set.
    # Replace with actual image content for testing.
    try:
        with open("example.jpg", "rb") as image_file:
            content = image_file.read()
        detected_text = detect_image_text(content)
        print("Detected text:", detected_text)
    except FileNotFoundError:
        print("example.jpg not found. Please create an example image file or provide actual image content.")
    except Exception as e:
        print(f"An error occurred: {e}")
