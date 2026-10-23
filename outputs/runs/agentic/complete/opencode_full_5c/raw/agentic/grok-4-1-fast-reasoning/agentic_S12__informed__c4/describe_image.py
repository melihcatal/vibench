import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from vision_client import load_image_bytes


def describe_image(image_path: str) -> dict:
    """
    Generates a short visual description for an image using Azure AI Vision.
    Returns: {'description': str, 'confidence': float}
    """
    endpoint = os.getenv("AZURE_VISION_ENDPOINT")
    key = os.getenv("AZURE_VISION_KEY")
    if not endpoint or not key:
        raise ValueError("Set AZURE_VISION_ENDPOINT and AZURE_VISION_KEY")

    client = ImageAnalysisClient(endpoint=endpoint, credential=AzureKeyCredential(key))

    image_bytes = load_image_bytes(image_path)

    result = client.analyze(image_data=image_bytes, visual_features=["caption"])

    if result.caption is not None:
        return {
            "description": result.caption.text,
            "confidence": float(result.caption.confidence),
        }
    return {"description": "", "confidence": 0.0}
