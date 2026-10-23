import os


def load_image_bytes(image_path: str) -> bytes:
    with open(image_path, "rb") as f:
        return f.read()


def get_google_vision_client():
    from google.cloud import vision

    return vision.ImageAnnotatorClient()


def get_azure_vision_client():
    from azure.ai.vision.imageanalysis import ImageAnalysisClient
    from azure.core.credentials import AzureKeyCredential

    endpoint = os.getenv("AZURE_VISION_ENDPOINT")
    key = os.getenv("AZURE_VISION_KEY")
    return ImageAnalysisClient(endpoint=endpoint, credential=AzureKeyCredential(key))


def get_rekognition_client():
    import boto3

    return boto3.client(
        "rekognition",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name="us-east-1",
    )
