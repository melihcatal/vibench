"""
describe_image.py - Generates a short visual description for an image
using Azure AI Vision Image Analysis SDK.
"""

import sys
from typing import Optional

from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential

from vision_client import (
    create_image_analysis_client,
    read_image_bytes,
)
from vision_models import ImageDescription, normalize_description_from_azure


def describe_image(
    image_path: str,
    *,
    client: Optional[ImageAnalysisClient] = None,
) -> ImageDescription:
    """
    Generate a short visual description for a static image using Azure AI Vision.

    Provider: Azure AI Vision (azure-ai-vision-imageanalysis)
    Auth: AZURE_VISION_ENDPOINT, AZURE_VISION_KEY
    """
    if client is None:
        client = create_image_analysis_client()

    image_bytes = read_image_bytes(image_path)

    features = [
        VisualFeatures.CAPTION,
        VisualFeatures.TAGS,
    ]

    result = client.analyze(
        image_data=image_bytes,
        visual_features=features,
    )

    caption_obj = None
    if result.caption is not None and result.caption.text:
        caption_obj = result.caption

    tags_list = []
    if result.tags is not None:
        tags_list = [tag.name for tag in result.tags if tag.name]

    if caption_obj:
        description = ImageDescription(
            text=caption_obj.text or "",
            confidence=float(caption_obj.confidence or 0.0),
            tags=tags_list,
        )
    else:
        description = ImageDescription(
            text="",
            confidence=0.0,
            tags=tags_list,
        )

    return description


def format_description_report(description: ImageDescription) -> str:
    """Format image description into a human-readable report."""
    lines = []
    if description.text:
        lines.append(f"Description: {description.text}")
        lines.append(f"Confidence: {description.confidence:.2%}")
    else:
        lines.append("No description generated.")

    if description.tags:
        lines.append(f"Tags: {', '.join(description.tags)}")

    return "\n".join(lines)


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python describe_image.py <image_path>")
        sys.exit(1)

    image_path = sys.argv[1]
    description = describe_image(image_path)
    report = format_description_report(description)
    print(report)


if __name__ == "__main__":
    main()
