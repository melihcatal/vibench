import os
from azure.ai.vision.imageanalysis import ImageAnalysisClient, ImageAnalysisOptions, VisualFeatures
from azure.core.credentials import AzureKeyCredential

def run_ocr_on_stored_document(image_url: str) -> str:
    """
    Runs OCR on a stored document object using Azure AI Vision.

    Args:
        image_url (str): The publicly accessible URL of the image to perform OCR on.

    Returns:
        str: The extracted text from the document.
    """
    endpoint = os.environ.get("AZURE_VISION_ENDPOINT")
    key = os.environ.get("AZURE_VISION_KEY")

    if not endpoint or not key:
        raise ValueError("AZURE_VISION_ENDPOINT and AZURE_VISION_KEY environment variables must be set.")

    client = ImageAnalysisClient(endpoint=endpoint, credential=AzureKeyCredential(key))

    # Select the features to analyze
    features = [VisualFeatures.READ]

    # Analyze the image URL
    result = client.analyze_from_url(image_url=image_url, visual_features=features)

    if result.read is not None:
        extracted_text = "\n".join([line.text for line in result.read.blocks[0].lines])
        return extracted_text
    else:
        return "No text found in the document."
