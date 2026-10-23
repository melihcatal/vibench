import os
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential
from storage_client import AzureBlobStorageClient
from storage_models import StoredDocumentOcrRequest, StoredDocumentOcrResponse
from azure.core.exceptions import ResourceNotFoundError
from dotenv import load_dotenv

load_dotenv()

def stored_document_ocr(request: StoredDocumentOcrRequest) -> StoredDocumentOcrResponse:
    endpoint = os.getenv("AZURE_VISION_ENDPOINT")
    key = os.getenv("AZURE_VISION_KEY")

    if not endpoint or not key:
        return StoredDocumentOcrResponse(success=False, error="AZURE_VISION_ENDPOINT or AZURE_VISION_KEY environment variables not set.")

    vision_client = ImageAnalysisClient(endpoint=endpoint, credential=AzureKeyCredential(key))
    storage_client = AzureBlobStorageClient()

    try:
        blob_client = storage_client.get_blob_client(request.container_name, request.blob_name)
        # Get the URL of the blob for OCR processing
        blob_url = blob_client.url

        # Analyze the image for text content
        result = vision_client.analyze(url=blob_url, visual_features=[VisualFeatures.READ])

        if result.read and result.read.blocks:
            text_content = "\n".join([line.text for block in result.read.blocks for line in block.lines])
            return StoredDocumentOcrResponse(success=True, text_content=text_content)
        else:
            return StoredDocumentOcrResponse(success=True, text_content="No text found in the document.")

    except ResourceNotFoundError:
        return StoredDocumentOcrResponse(success=False, error=f"Blob '{request.blob_name}' not found in container '{request.container_name}'.")
    except Exception as e:
        return StoredDocumentOcrResponse(success=False, error=str(e))
