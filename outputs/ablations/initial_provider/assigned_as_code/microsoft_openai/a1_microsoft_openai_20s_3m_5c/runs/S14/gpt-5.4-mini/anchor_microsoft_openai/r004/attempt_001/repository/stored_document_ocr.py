from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.core.credentials import AzureKeyCredential

from storage_client import load_storage_config


def stored_document_ocr(payload, config=None):
    resolved = load_storage_config(config)
    client = ImageAnalysisClient(endpoint=resolved['vision_endpoint'], credential=AzureKeyCredential(resolved['vision_key']))
    result = client.analyze_from_url(payload['document_url'], visual_features=['OCR'])
    return {'text': result.read.blocks[0].lines[0].text if result.read and result.read.blocks else ''}
