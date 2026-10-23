import os
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential

from storage_client import get_blob_client
from storage_models import StoredDocumentOcrRequest, StoredDocumentOcrResponse

def stored_document_ocr(request: StoredDocumentOcrRequest) -> StoredDocumentOcrResponse:
    endpoint = os.getenv("AZURE_VISION_ENDPOINT")
    key = os.getenv("AZURE_VISION_KEY")

    if not endpoint or not key:
        raise ValueError("AZURE_VISION_ENDPOINT and AZURE_VISION_KEY environment variables not set.")

    blob_client = get_blob_client(request.container_name, request.blob_name)
    download_stream = blob_client.download_blob()
    image_data = download_stream.readall()

    client = ImageAnalysisClient(endpoint=endpoint, credential=AzureKeyCredential(key))
    
    # Analyze a local image file
    result = client.analyze(image_data, visual_features=[VisualFeatures.READ])
    
    extracted_text = ""
    if result.read and result.read.blocks:
        for block in result.read.blocks:
            for line in block.lines:
                extracted_text += line.text + "\n"

    return StoredDocumentOcrResponse(text=extracted_text.strip())
