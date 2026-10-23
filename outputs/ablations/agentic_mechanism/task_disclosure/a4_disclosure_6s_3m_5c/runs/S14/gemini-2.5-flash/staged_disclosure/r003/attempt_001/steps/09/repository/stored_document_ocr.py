
from google.cloud import vision

def detect_document_text_from_gcs(gcs_uri: str) -> str:
    """Performs document text detection on a document stored in Google Cloud Storage."""
    client = vision.ImageAnnotatorClient()
    image = vision.Image()
    image.source.image_uri = gcs_uri

    response = client.document_text_detection(image=image)
    return response.full_text_annotation.text

if __name__ == "__main__":
    # Replace with your Google Cloud Storage URI
    # Example: "gs://cloud-samples-data/vision/document/commercial_invoice.pdf"
    gcs_document_uri = "gs://your-bucket-name/your-document.pdf"
    
    print(f"Performing OCR on document: {gcs_document_uri}")
    try:
        extracted_text = detect_document_text_from_gcs(gcs_document_uri)
        print("Extracted Text:")
        print(extracted_text)
    except Exception as e:
        print(f"An error occurred: {e}")
        print("Please ensure you have authenticated to Google Cloud and the GCS URI is correct.")
