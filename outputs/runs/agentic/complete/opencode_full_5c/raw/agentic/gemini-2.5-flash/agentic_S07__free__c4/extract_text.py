from google.cloud import vision_v1p4beta1 as vision
from document_client import get_vision_client
from document_models import DocumentInput, ExtractedText


def extract_text_from_image(document_input: DocumentInput) -> ExtractedText:
    client = get_vision_client()

    if document_input.gcs_source:
        image = vision.Image(
            source=vision.ImageSource(gcs_image_uri=document_input.gcs_source)
        )
    elif document_input.content:
        image = vision.Image(content=document_input.content)
    else:
        raise ValueError("Either gcs_source or content must be provided.")

    response = client.document_text_detection(image=image)
    return ExtractedText(text=response.full_text_annotation.text)
