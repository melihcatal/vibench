import os
from google.cloud import vision_v1p4beta1 as vision
from document_client import get_vision_client
from document_models import DocumentTextResponse

def extract_plain_text(image_content: bytes) -> DocumentTextResponse:
    client = get_vision_client()

    image = vision.Image(content=image_content)
    feature = vision.Feature(type_=vision.Feature.Type.TEXT_DETECTION)
    request = vision.AnnotateImageRequest(image=image, features=[feature])

    response = client.annotate_image(request=request)

    full_text = response.full_text_annotation.text if response.full_text_annotation else ""
    
    return DocumentTextResponse(text=full_text)
