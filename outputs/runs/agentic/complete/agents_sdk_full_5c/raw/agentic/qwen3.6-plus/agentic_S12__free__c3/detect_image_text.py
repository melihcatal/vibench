"""
Detect text appearing inside an image using Google Cloud Vision API.
Provider: Google Cloud Vision (vision.googleapis.com) - DOCUMENT_TEXT_DETECTION
"""

from typing import List, Optional

from google.cloud import vision as gc_vision

from vision_client import get_google_vision_client, load_image_bytes
from vision_models import DetectedText, ImageAnalysisPayload


def detect_text_in_image(
    image_path: Optional[str] = None,
    image_bytes: Optional[bytes] = None,
    language_hints: Optional[List[str]] = None,
) -> ImageAnalysisPayload:
    """
    Detect and extract text from a static image using Google Cloud Vision OCR.

    Uses the DOCUMENT_TEXT_DETECTION feature for high-quality text recognition,
    with support for dense text and various document formats.

    Args:
        image_path: Path to the image file.
        image_bytes: Raw image bytes.
        language_hints: Optional list of BCP-47 language codes (e.g., ['en', 'es']).

    Returns:
        ImageAnalysisPayload containing detected text annotations.
    """
    raw_image = load_image_bytes(image_path=image_path, image_bytes=image_bytes)
    client = get_google_vision_client()

    image = gc_vision.Image(content=raw_image)
    image_context = gc_vision.ImageContext(
        language_hints=language_hints or ["en"]
    )

    response = client.document_text_detection(
        image=image,
        image_context=image_context,
    )

    texts = []
    full_text = response.full_text_annotation.text if response.full_text_annotation else ""

    for page in response.full_text_annotation.pages if response.full_text_annotation else []:
        for block in page.blocks:
            for paragraph in block.paragraphs:
                for word in paragraph.words:
                    word_text = "".join(
                        symbol.text for symbol in word.symbols
                    )
                    if word_text.strip():
                        confidence = word.confidence if hasattr(word, "confidence") else 1.0
                        detected = DetectedText(
                            text=word_text,
                            confidence=confidence,
                        )
                        texts.append(detected)

    payload = ImageAnalysisPayload(
        image_path=image_path,
        detected_texts=texts,
        metadata={
            "provider": "google_cloud_vision",
            "ocr_feature": "DOCUMENT_TEXT_DETECTION",
            "api_endpoint": "vision.googleapis.com",
            "full_text": full_text,
            "text_blocks_detected": len(texts),
        },
    )

    return payload


def detect_text_sparse(
    image_path: Optional[str] = None,
    image_bytes: Optional[bytes] = None,
    language_hints: Optional[List[str]] = None,
) -> ImageAnalysisPayload:
    """
    Detect text using TEXT_DETECTION (sparse text, signage, labels).

    Args:
        image_path: Path to the image file.
        image_bytes: Raw image bytes.
        language_hints: Optional language hints.

    Returns:
        ImageAnalysisPayload with detected text.
    """
    raw_image = load_image_bytes(image_path=image_path, image_bytes=image_bytes)
    client = get_google_vision_client()

    image = gc_vision.Image(content=raw_image)
    image_context = gc_vision.ImageContext(
        language_hints=language_hints or ["en"]
    )

    response = client.text_detection(
        image=image,
        image_context=image_context,
    )

    texts = []
    for annotation in response.text_annotations:
        detected = DetectedText.from_google_vision(annotation)
        texts.append(detected)

    return ImageAnalysisPayload(
        image_path=image_path,
        detected_texts=texts,
        metadata={
            "provider": "google_cloud_vision",
            "ocr_feature": "TEXT_DETECTION",
            "api_endpoint": "vision.googleapis.com",
            "text_annotations": len(texts),
        },
    )


def extract_full_text(
    payload: ImageAnalysisPayload,
    join_with: str = " ",
) -> str:
    """
    Extract full text content from OCR results.

    Args:
        payload: ImageAnalysisPayload from detect_text_in_image.
        join_with: String to join text segments.

    Returns:
        Combined text string.
    """
    return join_with.join(dt.text for dt in payload.detected_texts)


def get_high_confidence_text(
    payload: ImageAnalysisPayload,
    min_confidence: float = 0.8,
) -> List[DetectedText]:
    """
    Filter detected text by confidence threshold.

    Args:
        payload: ImageAnalysisPayload from detect_text_in_image.
        min_confidence: Minimum confidence threshold.

    Returns:
        List of high-confidence DetectedText objects.
    """
    return [
        dt for dt in payload.detected_texts
        if dt.confidence >= min_confidence
    ]


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        result = detect_text_in_image(image_path=sys.argv[1])
        full_text = result.metadata.get("full_text", "")
        print(full_text)
