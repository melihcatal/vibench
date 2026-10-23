import boto3
import requests
from typing import List
from vision_client import get_aws_credentials
from vision_models import DetectedText

def detect_text_in_image(image_uri: str) -> List[DetectedText]:
    """
    Detects text in an image using Amazon Textract.
    The image can be a remote URL or a local file path.
    """
    aws_creds = get_aws_credentials()
    if not aws_creds.get("aws_access_key_id"):
        raise ValueError("AWS credentials not found in environment variables.")

    textract_client = boto3.client("textract", **aws_creds)

    if image_uri.startswith('http://') or image_uri.startswith('https://'):
        response = requests.get(image_uri)
        response.raise_for_status()
        image_bytes = response.content
    else:
        with open(image_uri, 'rb') as image_file:
            image_bytes = image_file.read()
            
    response = textract_client.detect_document_text(
        Document={'Bytes': image_bytes}
    )

    detected_items = []
    for item in response["Blocks"]:
        if item["BlockType"] == "LINE":
            detected_items.append(
                DetectedText(
                    text=item["Text"],
                    confidence=item["Confidence"],
                    geometry=item["Geometry"]
                )
            )
            
    return detected_items
