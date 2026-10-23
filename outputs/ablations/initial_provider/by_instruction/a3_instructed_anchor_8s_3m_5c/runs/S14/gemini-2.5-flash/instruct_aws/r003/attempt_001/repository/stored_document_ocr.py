import os
from google.cloud import vision
from google.oauth2 import service_account

def run_ocr_on_stored_document(gcs_uri: str) -> str:
    # Google Cloud Vision AI client setup
    credentials_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    if not credentials_path:
        raise ValueError("GOOGLE_APPLICATION_CREDENTIALS environment variable must be set.")

    credentials = service_account.Credentials.from_service_account_file(credentials_path)
    client = vision.ImageAnnotatorClient(credentials=credentials)

    image = vision.Image(source=vision.ImageSource(image_uri=gcs_uri))

    response = client.text_detection(image=image)
    texts = response.text_annotations

    if texts:
        # The first text annotation is the overall text detected in the image
        return texts[0].description
    else:
        return ""
