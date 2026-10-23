import os
from google.cloud import vision

def detect_document_text_from_gcs(gcs_uri: str):
    """Detects document features in an image stored in Google Cloud Storage.

    Args:
        gcs_uri: The URI of the image in Google Cloud Storage.
                Format: gs://bucket-name/object-name
    """
    client = vision.ImageAnnotatorClient()
    image = vision.Image()
    image.source.image_uri = gcs_uri

    response = client.document_text_detection(image=image)
    full_text_annotation = response.full_text_annotation

    print(f"Full text: {full_text_annotation.text}")

    if response.error.message:
        raise Exception(
            "{}
For more info on error messages, check: "
            "https://cloud.google.com/apis/design/errors".format(response.error.message)
        )

if __name__ == "__main__":
    # Replace with your GCS URI, e.g., "gs://cloud-samples-data/vision/document/commercial_invoice.pdf"
    # Ensure you have authenticated to Google Cloud (e.g., gcloud auth application-default login)
    # and enabled the Vision AI API in your Google Cloud project.
    gcs_document_uri = os.environ.get("GCS_DOCUMENT_URI")
    if gcs_document_uri:
        detect_document_text_from_gcs(gcs_document_uri)
    else:
        print("Please set the GCS_DOCUMENT_URI environment variable.")
