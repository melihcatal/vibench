import os
from google.cloud import vision

def detect_document_text_from_gcs(gcs_uri: str):
    """Detects document text in the image located in Google Cloud Storage or on the
    Web."""
    client = vision.ImageAnnotatorClient()
    image = vision.Image()
    image.source.image_uri = gcs_uri

    response = client.document_text_detection(image=image)
    full_text_annotation = response.full_text_annotation
    
    # You can print the full text or process it further
    print(f"Full document text: {full_text_annotation.text}")

    if response.error.message:
        raise Exception(
            "{}\nFor more info on error messages, check: "
            "https://cloud.google.com/apis/design/errors".format(response.error.message)
        )

if __name__ == "__main__":
    # Replace with your GCS URI, e.g., "gs://cloud-samples-data/vision/document/commercial_invoice.pdf"
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set or
    # authenticated via `gcloud auth application-default login`
    gcs_document_uri = os.environ.get("GCS_DOCUMENT_URI", "gs://cloud-samples-data/vision/document/commercial_invoice.pdf")
    detect_document_text_from_gcs(gcs_document_uri)
