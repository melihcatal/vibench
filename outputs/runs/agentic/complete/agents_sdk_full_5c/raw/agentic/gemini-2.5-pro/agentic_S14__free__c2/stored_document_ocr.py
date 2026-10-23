from google.cloud import vision
from storage_models import OcrResult

def ocr_document_in_storage(gcs_uri: str) -> OcrResult:
    """
    Performs OCR on a document stored in Google Cloud Storage.

    :param gcs_uri: The GCS URI of the document (e.g., 'gs://bucket_name/path/to/file.pdf').
    :return: An OcrResult containing the extracted text and language.
    """
    client = vision.ImageAnnotatorClient()

    gcs_source = vision.GcsSource(uri=gcs_uri)
    # Supported MIME types include: "application/pdf", "image/tiff", "image/gif"
    feature = vision.Feature(type_=vision.Feature.Type.DOCUMENT_TEXT_DETECTION)
    
    input_config = vision.InputConfig(
        gcs_source=gcs_source,
        mime_type='application/pdf'  # Adjust if processing other types
    )

    request = vision.AnnotateFileRequest(
        input_config=input_config,
        features=[feature]
    )

    # For large documents, use async_batch_annotate_files
    # For this example, we assume a single file that fits sync processing
    response = client.batch_annotate_files(requests=[request])

    full_text = ""
    detected_language = "und"

    # Assuming one file in the batch request
    for image_response in response.responses[0].responses:
        full_text += image_response.full_text_annotation.text
        if image_response.full_text_annotation.pages:
            page = image_response.full_text_annotation.pages[0]
            if page.property and page.property.detected_languages:
                detected_language = page.property.detected_languages[0].language_code

    return OcrResult(
        source_uri=gcs_uri,
        text=full_text,
        language=detected_language
    )
