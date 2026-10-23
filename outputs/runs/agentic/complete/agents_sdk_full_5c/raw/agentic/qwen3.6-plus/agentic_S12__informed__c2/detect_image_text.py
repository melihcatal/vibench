"""
detect_image_text.py - Detects text appearing inside an image
using Azure AI Vision Image Analysis SDK (OCR).
"""

import sys
from typing import List, Optional

from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential

from vision_client import (
    create_image_analysis_client,
    read_image_bytes,
)
from vision_models import DetectedTextRegion


def detect_image_text(
    image_path: str,
    *,
    confidence_threshold: float = 0.5,
    client: Optional[ImageAnalysisClient] = None,
) -> List[DetectedTextRegion]:
    """
    Detect and extract text appearing inside an image using Azure AI Vision OCR.

    Provider: Azure AI Vision (azure-ai-vision-imageanalysis)
    Auth: AZURE_VISION_ENDPOINT, AZURE_VISION_KEY
    """
    if client is None:
        client = create_image_analysis_client()

    image_bytes = read_image_bytes(image_path)

    result = client.analyze(
        image_data=image_bytes,
        visual_features=[VisualFeatures.READ],
    )

    text_regions: List[DetectedTextRegion] = []

    if result.read is not None:
        for line in result.read.blocks:
            for word in line.words:
                conf = word.confidence if word.confidence is not None else 0.0
                if conf >= confidence_threshold:
                    bounding_box = None
                    if word.bounding_polygon is not None:
                        pts = word.bounding_polygon
                        bounding_box = [
                            int(getattr(pts, attr, 0))
                            for attr in ("x", "y", "width", "height")
                        ]
                    region = DetectedTextRegion(
                        text=word.text or "",
                        confidence=float(conf),
                        bounding_box=bounding_box,
                    )
                    text_regions.append(region)

    text_regions.sort(key=lambda r: r.confidence, reverse=True)
    return text_regions


def format_text_report(text_regions: List[DetectedTextRegion]) -> str:
    """Format detected text into a human-readable report."""
    if not text_regions:
        return "No text detected above the confidence threshold."

    lines = ["Detected Text:"]
    for region in text_regions:
        bbox_info = ""
        if region.bounding_box:
            bbox_info = f" [box: {region.bounding_box}]"
        lines.append(
            f"  - \"{region.text}\" ({region.confidence:.2%}){bbox_info}"
        )
    return "\n".join(lines)


def extract_full_text(text_regions: List[DetectedTextRegion]) -> str:
    """Concatenate all detected text into a single string."""
    return " ".join(region.text for region in text_regions if region.text)


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python detect_image_text.py <image_path> [confidence_threshold]")
        sys.exit(1)

    image_path = sys.argv[1]
    threshold = float(sys.argv[2]) if len(sys.argv) > 2 else 0.5

    text_regions = detect_image_text(image_path, confidence_threshold=threshold)
    report = format_text_report(text_regions)
    print(report)


if __name__ == "__main__":
    main()
