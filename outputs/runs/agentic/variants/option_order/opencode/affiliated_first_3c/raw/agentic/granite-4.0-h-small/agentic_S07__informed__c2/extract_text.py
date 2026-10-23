import os
import json
from document_client import OcrClient


def extract_text(image_path: str) -> str:
    """Extract plain text from a scanned document image using a cloud OCR provider.

    This implementation uses Google Document AI as the concrete provider.
    Set the environment variable GOOGLE_APPLICATION_CREDENTIALS to the path of your JSON credential file.
    """
    client = OcrClient()  # client internally uses google-cloud-documentai SDK
    response = client.async_batch_annotate_files(
        sources=[client.gcs_source(uri=f"gs://{os.getenv('GCS_BUCKET')}/{image_path}")]
    )
    # response is a list of documents; take the first
    document = response[0]
    # Normalize tokens to plain text
    text = "".join(page.text for page in document.pages)
    return text
