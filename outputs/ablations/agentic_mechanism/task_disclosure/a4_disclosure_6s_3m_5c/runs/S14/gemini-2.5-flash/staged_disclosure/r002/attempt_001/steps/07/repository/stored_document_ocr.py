import os
from google.cloud import vision

def detect_document_text_from_gcs(gcs_uri):
    """Detects document text in the image located in Google Cloud Storage or on the
    Web."""
    client = vision.ImageAnnotatorClient()
    image = vision.Image()
    image.source.image_uri = gcs_uri

    response = client.document_text_detection(image=image)
    
    # For a full list of available properties, see the document API reference
    # https://cloud.google.com/vision/docs/reference/rest/v1/TextAnnotation
    return response.full_text_annotation

if __name__ == '__main__':
    # Replace with your Google Cloud Storage URI
    gcs_document_uri = "gs://cloud-samples-data/vision/document/commercial_invoice.pdf" 
    
    # Set up Google Cloud authentication
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/key.json"

    document_text = detect_document_text_from_gcs(gcs_document_uri)
    print("Document Text:")
    print(document_text.text)
