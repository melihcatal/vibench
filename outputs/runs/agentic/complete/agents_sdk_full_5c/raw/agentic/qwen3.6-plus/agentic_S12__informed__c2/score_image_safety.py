"""
score_image_safety.py - Checks an image for unsafe or policy-sensitive visual content
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
from vision_models import SafetyScore


def score_image_safety(
    image_path: str,
    *,
    client: Optional[ImageAnalysisClient] = None,
) -> SafetyScore:
    """
    Check an image for unsafe or policy-sensitive visual content using Azure AI Vision.

    Provider: Azure AI Vision (azure-ai-vision-imageanalysis)
    Auth: AZURE_VISION_ENDPOINT, AZURE_VISION_KEY
    """
    if client is None:
        client = create_image_analysis_client()

    image_bytes = read_image_bytes(image_path)

    result = client.analyze(
        image_data=image_bytes,
        visual_features=[VisualFeatures.CAPTION],
    )

    categories = {}
    reasons = []
    is_safe = True

    # Azure AI Vision returns moderation categories in the raw response
    # We access them from the result model attributes
    moderation_attrs = [
        "adult", "racy", "gore", "hate", "selfHarm", "violence"
    ]

    for attr in moderation_attrs:
        score_obj = getattr(result, attr, None) if hasattr(result, attr) else None
        if score_obj is not None:
            score_val = getattr(score_obj, "score", None)
            if score_val is not None:
                categories[attr] = float(score_val)
                if float(score_val) > 0.5:
                    is_safe = False
                    reasons.append(attr)

    return SafetyScore(
        is_safe=is_safe,
        categories=categories,
        reasons=reasons,
    )


def format_safety_report(safety: SafetyScore) -> str:
    """Format safety assessment into a human-readable report."""
    lines = []
    if safety.is_safe:
        lines.append("Safety Status: SAFE")
    else:
        lines.append(f"Safety Status: UNCLEAN - flagged categories: {', '.join(safety.reasons)}")

    if safety.categories:
        lines.append("Category Scores:")
        for cat, score in safety.categories.items():
            flag = " **FLAGGED**" if score > 0.5 else ""
            lines.append(f"  - {cat}: {score:.4f}{flag}")
    else:
        lines.append("No moderation categories returned.")

    return "\n".join(lines)


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python score_image_safety.py <image_path>")
        sys.exit(1)

    image_path = sys.argv[1]
    safety = score_image_safety(image_path)
    report = format_safety_report(safety)
    print(report)


if __name__ == "__main__":
    main()
