from google.cloud import vision
from storage_models import OcrResult

def ocr_gcs_document(gcs_uri: str) -> OcrResult:
    """
    Performs OCR on a document stored in Google Cloud Storage.

    Args:
        gcs_uri (str): The GCS URI of the document (e.g., 'gs://bucket_name/path/to/doc.pdf').

    Returns:
        An OcrResult containing the extracted text.
    """
    if not gcs_uri.startswith("gs://"):
        raise ValueError("Invalid GCS URI. It must start with 'gs://'.")

    client = vision.ImageAnnotatorClient()

    # Supported mime_types: "application/pdf", "image/tiff", "image/gif"
    gcs_source = vision.GcsSource(uri=gcs_uri)
    feature = vision.Feature(type_=vision.Feature.Type.DOCUMENT_TEXT_DETECTION)
    
    input_config = vision.InputConfig(
        gcs_source=gcs_source, mime_type="application/pdf"
    )

    request = vision.AnnotateFileRequest(
        input_config=input_config,
        features=[feature]
    )

    response = client.batch_annotate_files(requests=[request])

    full_text = ""
    # Assuming one document per request
    for page_response in response.responses[0].responses:
        full_text += page_response.full_text_annotation.text

    return OcrResult(
        source_uri=gcs_uri,
        text=full_text
    )
