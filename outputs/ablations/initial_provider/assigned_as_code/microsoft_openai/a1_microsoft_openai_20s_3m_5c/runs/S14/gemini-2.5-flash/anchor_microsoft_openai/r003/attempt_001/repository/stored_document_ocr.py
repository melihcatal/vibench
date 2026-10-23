from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential
from storage_client import get_blob_client
from storage_models import ConfigType, PayloadType
import os

def stored_document_ocr(payload: PayloadType, config: ConfigType = None) -> PayloadType:
    config = config or {}
    # Azure AI Vision endpoint and key from config or environment variables
    endpoint = config.get("azure_vision_endpoint", os.environ.get("AZURE_VISION_ENDPOINT"))
    key = config.get("azure_vision_key", os.environ.get("AZURE_VISION_KEY"))
    container_name = config.get("container_name", payload.get("container_name"))
    object_name = payload["object_name"]

    if not all([endpoint, key, container_name, object_name]):
        raise ValueError("Missing required parameters: Azure Vision endpoint, key, container name, object name.")

    # Construct the URL for the blob
    account_url = config.get("account_url", os.environ.get("AZURE_STORAGE_ACCOUNT_URL"))
    if not account_url:
        raise ValueError("Azure Storage Account URL not provided and not found in environment variables.")
    blob_url = f"{account_url}/{container_name}/{object_name}"

    # Authenticate and create client
    credential = AzureKeyCredential(key)
    client = ImageAnalysisClient(endpoint=endpoint, credential=credential)

    # Perform OCR
    # Using `features=[VisualFeatures.READ]` for OCR
    # The SDK will download the image from the URL provided.
    try:
        result = client.analyze_from_url(image_url=blob_url, visual_features=[VisualFeatures.READ])
    except Exception as e:
        return {"error": f"Azure AI Vision OCR failed: {str(e)}"}

    extracted_text = []
    if result.read and result.read.blocks:
        for block in result.read.blocks:
            for line in block.lines:
                extracted_text.append(line.text)

    return {"extracted_text": "\n".join(extracted_text)}
