import os
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.core.credentials import AzureKeyCredential
from . import presigned_download
from . import storage_models

def ocr_from_stored_document(object_name: str) -> storage_models.OcrResult:
    """
    Performs OCR on a document stored in object storage using Azure AI Vision.

    Args:
        object_name: The name/key of the object in the bucket.

    Returns:
        An OcrResult containing the extracted text.
    """
    vision_endpoint = os.environ.get("AZURE_VISION_ENDPOINT")
    vision_key = os.environ.get("AZURE_VISION_KEY")

    if not vision_endpoint or not vision_key:
        raise ValueError("Azure Vision endpoint and key must be set in environment variables.")

    # 1. Get a temporary public URL for the private object
    document_url = presigned_download.generate_presigned_url(object_name)

    # 2. Authenticate with Azure AI Vision
    client = ImageAnalysisClient(
        endpoint=vision_endpoint,
        credential=AzureKeyCredential(vision_key)
    )

    # 3. Analyze the image from the URL to read text
    result = client.analyze(
        image_url=document_url,
        visual_features=["read"],
    )

    extracted_text = ""
    if result.read is not None:
        extracted_text = "\n".join([line.text for line in result.read.blocks[0].lines])

    return storage_models.OcrResult(
        source_uri=f"gs://{os.environ.get('GCS_BUCKET_NAME')}/{object_name}",
        text_content=extracted_text
    )
