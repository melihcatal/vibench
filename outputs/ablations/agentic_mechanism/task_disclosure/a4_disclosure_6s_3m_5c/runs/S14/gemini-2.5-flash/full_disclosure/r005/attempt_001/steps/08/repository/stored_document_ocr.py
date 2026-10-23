from google.cloud import vision

def run_ocr_on_document(gcs_uri: str) -> dict:
    """
    Runs OCR on a document stored in Google Cloud Storage.

    Args:
        gcs_uri: The Google Cloud Storage URI of the document (e.g., "gs://your-bucket-name/your-document-file").

    Returns:
        A dictionary containing the OCR results.
    """
    client = vision.ImageAnnotatorClient()
    image = vision.Image(source=vision.ImageSource(gcs_uri=gcs_uri))

    response = client.document_text_detection(image=image)
    
    # You can process the response further to extract specific text or annotations
    # For now, we'll return the full response as a dictionary.
    return response.text_annotations[0].description
