"""
extract_text.py - Extracts plain text from a scanned document image
using Azure Computer Vision API (Image Analysis SDK).

Provider: Azure AI Vision - Image Analysis
Model: read-4.0 (OCR model in Azure Computer Vision)
"""

from typing import Optional, Dict, Any, Union

from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError

from document_client import (
    DocumentClientConfig,
    get_azure_cv_client,
    normalize_image_to_bytes,
)
from document_models import OcrTextResult, normalize_azure_words_to_lines


def extract_text_from_image(
    image_data: Union[str, bytes, Any],
    language: str = "en",
    client: Optional[ImageAnalysisClient] = None,
) -> OcrTextResult:
    """
    Extract plain text from a scanned document image using Azure Computer Vision.

    Args:
        image_data: Image as bytes, file path string, or file-like object.
        language: BCP-47 language hint (default "en").
        client: Optional pre-configured ImageAnalysisClient instance.

    Returns:
        OcrTextResult with extracted text, lines, words, and confidence.
    """
    if client is None:
        client = get_azure_cv_client()

    image_bytes = normalize_image_to_bytes(image_data)

    try:
        result = client.analyze(
            image_data=image_bytes,
            visual_features=[VisualFeatures.READ],
            language=language,
        )
    except HttpResponseError as e:
        raise RuntimeError(f"Azure Computer Vision OCR failed: {e}") from e

    read_result = result.read
    if read_result is None:
        return OcrTextResult(
            extracted_text="",
            language=language,
            confidence=0.0,
        )

    all_text_parts = []
    all_words = []
    total_confidence = 0.0
    word_count = 0

    for line in read_result.blocks[0].lines if read_result.blocks else []:
        line_text = line.text if hasattr(line, "text") else ""
        all_text_parts.append(line_text)

        for word in line.words:
            word_text = word.text if hasattr(word, "text") else ""
            word_conf = word.confidence if hasattr(word, "confidence") else 0.0
            word_bbox = word.bounding_box if hasattr(word, "bounding_box") else []
            all_words.append({
                "text": word_text,
                "confidence": word_conf,
                "bounding_box": list(word_bbox) if word_bbox else [],
            })
            total_confidence += word_conf
            word_count += 1

    extracted_text = " ".join(all_text_parts)
    avg_confidence = total_confidence / word_count if word_count > 0 else 0.0

    lines_data = normalize_azure_words_to_lines(all_words)

    page_dimensions = None
    if read_result.model_version:
        page_dimensions = {
            "model_version": read_result.model_version,
        }

    return OcrTextResult(
        extracted_text=extracted_text,
        language=read_result.language if hasattr(read_result, "language") else language,
        confidence=avg_confidence,
        lines=lines_data,
        words=all_words,
        page_dimensions=page_dimensions,
    )


def extract_text_batch(
    image_paths: list,
    language: str = "en",
    client: Optional[ImageAnalysisClient] = None,
) -> list:
    """
    Extract text from multiple document images in sequence.

    Args:
        image_paths: List of image file paths or byte arrays.
        language: BCP-47 language hint.
        client: Optional pre-configured ImageAnalysisClient instance.

    Returns:
        List of OcrTextResult objects.
    """
    results = []
    for image in image_paths:
        result = extract_text_from_image(image, language=language, client=client)
        results.append(result)
    return results
