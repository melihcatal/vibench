# Generate a short visual description for an image using Amazon Rekognition
import os
import boto3
from vision_client import get_rekognition_client
from vision_models import normalize_description


def describe_image(image_path: str):
    """Generate a short description of an image using Amazon Rekognition."""
    client = get_rekognition_client()
    response = client.detect_labels(
        Image={
            "S3Object": {
                "Bucket": os.getenv("AWS_S3_BUCKET"),
                "Name": os.path.basename(image_path),
            }
        },
        MaxLabels=5,
        MinConfidence=70.0,
    )
    # Use the first label with highest confidence as a brief caption
    top_label = max(response["Labels"], key=lambda l: l["Confidence"])
    description = f"An image containing {top_label['Name']} with confidence {top_label['Confidence']:.1f}%"
    return normalize_description(description)
