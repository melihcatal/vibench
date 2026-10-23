from typing import Optional
from google.cloud import vision_v1
from google.api_core.client_options import ClientOptions
from document_client import (
    get_vision_client,
    build_image_request,
    GOOGLE_CLOUD_PROJECT_ID,
)
from document_models import OCRTextRequest, OCRTextResponse


VISION_API_ENDPOINT = "vision.googleapis.com"
GOOGLE_VISION_MODEL = "builtin/latest"


def extract_text_from_image(
    image_bytes: bytes,
    mime_type: str = "image/png",
    language_hint: Optional[str] = None,
) -> OCRTextResponse:
    client = get_vision_client()
    feature_types = [
        vision_v1.Feature.Type.TEXT_DETECTION,
        vision_v1.Feature.Type.DOCUMENT_TEXT_DETECTION,
    ]
    image = vision_v1.Image(content=image_bytes)
    image_context = vision_v1.ImageContext()
    if language_hint:
        image_context.language_hints = [language_hint]
    features = [vision_v1.Feature(type_=ft) for ft in feature_types]
    request = vision_v1.AnnotateImageRequest(
        image=image, features=features, image_context=image_context
    )
    response = client.annotate_image(request=request)
    full_text = ""
    confidence = 0.0
    block_count = 0
    for result in response.responses:
        if result.full_text_annotation:
            full_text = result.full_text_annotation.text
            for page in result.full_text_annotation.pages:
                for block in page.blocks:
                    confidence += block.confidence
                    block_count += 1
        elif result.text_annotations:
            if result.text_annotations:
                full_text = result.text_annotations[0].description
                confidence = (
                    result.text_annotations[0].confidence
                    if result.text_annotations
                    else 0.0
                )
    avg_confidence = confidence / block_count if block_count > 0 else 0.0
    return OCRTextResponse(
        text=full_text,
        confidence=avg_confidence,
        raw_response={"responses": [{"text": full_text}]},
    )


def extract_text_from_gcs_uri(
    gcs_uri: str,
    mime_type: str = "image/png",
    language_hint: Optional[str] = None,
) -> OCRTextResponse:
    client = get_vision_client()
    image = vision_v1.Image(source=vision_v1.ImageSource(image_uri=gcs_uri))
    image_context = vision_v1.ImageContext()
    if language_hint:
        image_context.language_hints = [language_hint]
    features = [
        vision_v1.Feature(type_=vision_v1.Feature.Type.DOCUMENT_TEXT_DETECTION),
        vision_v1.Feature(type_=vision_v1.Feature.Type.TEXT_DETECTION),
    ]
    request = vision_v1.AnnotateImageRequest(
        image=image, features=features, image_context=image_context
    )
    response = client.annotate_image(request=request)
    full_text = ""
    confidence = 0.0
    block_count = 0
    for result in response.responses:
        if result.full_text_annotation:
            full_text = result.full_text_annotation.text
            for page in result.full_text_annotation.pages:
                for block in page.blocks:
                    confidence += block.confidence
                    block_count += 1
    avg_confidence = confidence / block_count if block_count > 0 else 0.0
    return OCRTextResponse(
        text=full_text,
        confidence=avg_confidence,
        raw_response={"responses": [{"text": full_text}]},
    )
