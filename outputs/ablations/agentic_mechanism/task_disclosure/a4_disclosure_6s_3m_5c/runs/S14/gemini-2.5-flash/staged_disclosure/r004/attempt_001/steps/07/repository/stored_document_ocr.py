from google.cloud import vision

def detect_document_text_from_uri(gcs_uri: str) -> vision.FullTextAnnotation:
    """Detects document text in the file located in Google Cloud Storage or on the Web."""
    client = vision.ImageAnnotatorClient()
    image = vision.Image()
    image.source.image_uri = gcs_uri

    response = client.document_text_detection(image=image)
    return response.full_text_annotation

if __name__ == "__main__":
    # This is an example of how to use the function.
    # Replace with your actual GCS URI or a publicly accessible image URI.
    # For authentication, ensure your environment is configured with Google Cloud credentials.
    # For example, by running `gcloud auth application-default login`
    # or setting the GOOGLE_APPLICATION_CREDENTIALS environment variable.
    # Example GCS URI: "gs://cloud-samples-data/vision/document/commercial_invoice.pdf"
    document_uri = "gs://cloud-samples-data/vision/document/handwritten_invoice.pdf" 
    
    print(f"Performing OCR on: {document_uri}")
    try:
        full_text_annotation = detect_document_text_from_uri(document_uri)
        print("Full text from document:")
        print(full_text_annotation.text)
    except Exception as e:
        print(f"An error occurred: {e}")
        print("Please ensure the GCS URI is correct and you have appropriate permissions.")
