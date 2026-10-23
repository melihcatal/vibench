# detect_image_labels.py
"""Static Image & Visual Understanding: Detect image labels / objects using Azure AI Vision SDK."""

from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.core.credentials import AzureKeyCredential

# Provider identifiers (Azure AI Vision)
AZURE_VISION_ENDPOINT = "YOUR_ENDPOINT"
AZURE_VISION_KEY = "YOUR_KEY"


def detect_image_labels(image_path: str):
    """Detect objects/labels in a static image and return a list of detected labels.

    Args:
        image_path: Path to the local image file.

    Returns:
        List of dictionaries with 'name' and 'confidence' keys.
    """
    client = ImageAnalysisClient(
        endpoint=AZURE_VISION_ENDPOINT,
        credential=AzureKeyCredential(AZURE_VISION_KEY),
    )
    # Call the SDK to analyze the image for labels
    analysis = client.analyze_image(
        image=open(image_path, "rb"),
        visual_features=["Labels"],
    )
    # Normalize and return results
    return [
        {
            "name": label.name,
            "confidence": label.confidence,
        }
        for label in analysis.labels
    ]
