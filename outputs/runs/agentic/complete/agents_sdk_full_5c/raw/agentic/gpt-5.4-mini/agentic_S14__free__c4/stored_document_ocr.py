from __future__ import annotations

import os
from typing import Optional

from google.cloud import vision

from storage_client import get_bucket_name, get_s3_client
from storage_models import ObjectRef, TextDocument, safe_join_text

GOOGLE_VISION_MODEL = "google-cloud-vision"


def stored_document_ocr(key: str, language_hints: Optional[list[str]] = None) -> TextDocument:
    s3 = get_s3_client()
    bucket = get_bucket_name()
    obj = s3.get_object(Bucket=bucket, Key=key)
    content = obj["Body"].read()

    client = vision.ImageAnnotatorClient()
    image = vision.Image(content=content)
    context = vision.ImageContext(language_hints=language_hints or None)
    response = client.document_text_detection(image=image, image_context=context)
    text = response.full_text_annotation.text if response.full_text_annotation and response.full_text_annotation.text else safe_join_text(
        [annotation.description for annotation in response.text_annotations]
    )
    return TextDocument(source=ObjectRef(bucket=bucket, key=key), text=text, language=(language_hints[0] if language_hints else None), provider=GOOGLE_VISION_MODEL)
