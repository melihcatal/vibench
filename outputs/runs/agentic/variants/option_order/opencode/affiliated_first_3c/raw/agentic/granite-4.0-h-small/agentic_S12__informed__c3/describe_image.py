# [SAME-SCENARIO] describe_image.py
# Generate a short visual description for an image using Amazon Rekognition SDK
import os
import boto3
from boto3.session import Session


def describe_image(image_path: str) -> str:
    """Generate a concise description for the image.

    Args:
        image_path (str): Path to the local image file.

    Returns:
        str: Summarized description of the image content.
    """
    # boto3 will pick up credentials from environment (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
    client = boto3.client("rekognition")
    with open(image_path, "rb") as img:
        response = client.detect_labels(Image={"Bytes": img.read()})
    # Pick the top label as a simple description
    top_label = (
        response["Labels"][0]["Name"] if response["Labels"] else "No labels detected"
    )
    return f"Image depicts: {top_label}"


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: describe_image.py <image_path>")
        sys.exit(1)
    print(describe_image(sys.argv[1]))
