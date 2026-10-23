# [SAME-SCENARIO] detect_image_text.py
# Detect embedded text in an image using Azure AI Vision SDK
import os
from azure.ai.vision.imageanalysis import ImageAnalysisClient, VisionModel
from azure.identity import DefaultAzureCredential


def extract_text(image_path: str) -> list[str]:
    """Extract text from image using Azure AI Vision.

    Args:
        image_path (str): Path to the local image file.

    Returns:
        list[str]: List of detected text strings.
    """
    endpoint = os.getenv("AZURE_VISION_ENDPOINT")
    if not endpoint:
        raise RuntimeError("AZURE_VISION_ENDPOINT environment variable not set")
    credential = DefaultAzureCredential()
    client = ImageAnalysisClient(
        endpoint=endpoint, credential=credential, api_version="2023-02-01-preview"
    )
    with open(image_path, "rb") as img:
        result = client.read(image=img.read(), model=VisionModel.read)
    texts = result.read_results
    return [line.text for result in texts for line in result.lines]


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: detect_image_text.py <image_path>")
        sys.exit(1)
    print("Text found:", extract_text(sys.argv[1]))
