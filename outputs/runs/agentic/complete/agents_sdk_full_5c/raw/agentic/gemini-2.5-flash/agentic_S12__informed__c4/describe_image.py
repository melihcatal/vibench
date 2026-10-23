
import os
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential

def describe_image(image_content: bytes) -> str:
    """Generates a short visual description for an image using Azure AI Vision."""
    endpoint = os.environ.get("AZURE_VISION_ENDPOINT")
    key = os.environ.get("AZURE_VISION_KEY")

    if not endpoint or not key:
        raise ValueError("AZURE_VISION_ENDPOINT and AZURE_VISION_KEY environment variables must be set.")

    client = ImageAnalysisClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(key)
    )

    # Analyze the image for a description
    result = client.analyze(
        image_data=image_content,
        visual_features=[VisualFeatures.CAPTION]
    )

    if result.caption is not None:
        return result.caption.text
    return "No description found."

if __name__ == '__main__':
    # This is example usage.
    # Ensure AZURE_VISION_ENDPOINT and AZURE_VISION_KEY are set.
    # Replace with actual image content for testing.
    try:
        with open("example.jpg", "rb") as image_file:
            content = image_file.read()
        description = describe_image(content)
        print("Description:", description)
    except FileNotFoundError:
        print("example.jpg not found. Please create an example image file or provide actual image content.")
    except Exception as e:
        print(f"An error occurred: {e}")
