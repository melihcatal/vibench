from storage_client import get_vision_client, get_gcs_bucket_name
from storage_models import ExtractedText
from google.cloud import vision


def ocr_from_gcs_document(object_name: str) -> ExtractedText:
    """
    Performs OCR on a document stored in Google Cloud Storage.

    Args:
        object_name: The name of the document object in the GCS bucket.

    Returns:
        An ExtractedText object containing the source and extracted text.
    """
    vision_client = get_vision_client()
    bucket_name = get_gcs_bucket_name()

    gcs_uri = f"gs://{bucket_name}/{object_name}"

    image = vision.Image()
    image.source.image_uri = gcs_uri

    response = vision_client.document_text_detection(image=image)

    if response.error.message:
        raise Exception(
            f"{response.error.message}\nFor more info on error messages, check: "
            "https://cloud.google.com/apis/design/errors"
        )

    return ExtractedText(source_object=gcs_uri, text=response.full_text_annotation.text)
