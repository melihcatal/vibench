import os
from typing import List
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.core.credentials import AzureKeyCredential

from vision_models import ImageText, VisualAnalysis


def detect_text_in_image(image_url: str) -> List[ImageText]:
    """
    Detects and extracts text from an image using Azure AI Vision.

    Args:
        image_url: Publicly accessible URL of the image.

    Returns:
        A list of ImageText objects.
    """
    key = os.environ.get("AZURE_AI_VISION_KEY")
    endpoint = os.environ.get("AZURE_AI_VISION_ENDPOINT")

    if not key or not endpoint:
        raise ValueError("Azure AI Vision credentials are not set in environment variables.")

    client = ImageAnalysisClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(key)
    )

    result = client.analyze_from_url(image_url=image_url, visual_features=['text'])

    detected_texts = []
    if result.text is not None:
        for line in result.text.lines:
            for word in line.words:
                detected_texts.append(
                    ImageText(
                        text=word.text,
                        confidence=word.confidence,
                        bounding_box=[
                            (p.x, p.y) for p in word.bounding_polygon
                        ],
                        provider="azure_ai_vision"
                    )
                )

    return detected_texts


def detect_image_text(analysis: VisualAnalysis) -> VisualAnalysis:
    """Detects text and adds it to the analysis object."""
    if not analysis.source_uri:
        raise ValueError("Analysis object must have a source_uri")

    texts = detect_text_in_image(image_url=analysis.source_uri)
    analysis.texts = texts
    return analysis
