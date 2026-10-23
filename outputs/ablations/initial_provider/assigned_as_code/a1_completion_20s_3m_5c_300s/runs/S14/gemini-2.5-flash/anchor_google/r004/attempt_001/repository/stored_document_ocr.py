from google.cloud import vision
from google.cloud import storage
import os

def stored_document_ocr(payload: dict) -> dict:
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT_ID environment variable not set")

    client = vision.ImageAnnotatorClient()
    
    gcs_source_uri = f"gs://{payload['bucket_name']}/{payload['object_name']}"
    mime_type = payload.get("mime_type", "application/pdf") # Assume PDF if not provided

    # Set up the input configuration for the OCR operation.
    input_config = vision.InputConfig(gcs_source=vision.GcsSource(uri=gcs_source_uri), mime_type=mime_type)
    feature = vision.Feature(type_=vision.Feature.Type.DOCUMENT_TEXT_DETECTION)
    
    # For PDF and TIFF files, each page is treated as a separate image.
    # The max_pages parameter can limit the number of pages to process.
    image_context = vision.ImageContext(
        # Only process the first page, for example
        # page_numbers=[1]
    )

    request = vision.AnnotateFileRequest(input_config=input_config, features=[feature], image_context=image_context)

    response = client.annotate_file(request)

    full_text_annotations = []
    for page_response in response.responses:
        if page_response.full_text_annotation:
            full_text_annotations.append(page_response.full_text_annotation.text)
            
    return {"extracted_text": "\n".join(full_text_annotations)}
