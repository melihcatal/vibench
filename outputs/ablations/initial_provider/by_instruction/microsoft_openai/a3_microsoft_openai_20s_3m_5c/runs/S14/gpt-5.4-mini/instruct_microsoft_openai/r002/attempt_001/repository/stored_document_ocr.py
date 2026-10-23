import os

from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.core.credentials import AzureKeyCredential

from storage_client import get_blob_service_client, load_config, normalize_blob_name


def stored_document_ocr(blob_name: str, container: str = None) -> str:
    config = load_config(container)
    client = get_blob_service_client(config)
    blob = client.get_blob_client(container=config.container, blob=normalize_blob_name(blob_name)).download_blob().readall()
    vision_endpoint = os.environ["AZURE_AI_VISION_ENDPOINT"]
    vision_key = os.environ["AZURE_AI_VISION_KEY"]
    analysis_client = ImageAnalysisClient(endpoint=vision_endpoint, credential=AzureKeyCredential(vision_key))
    result = analysis_client.analyze(binary_data=blob, visual_features=["READ"])
    return "\n".join([line.text for block in getattr(result.read, "blocks", []) for line in getattr(block, "lines", [])])
