"""
Check an image for unsafe or policy-sensitive visual content using Azure Content Safety.
Provider: Azure Content Safety (content-safety.cognitiveservices.azure.com)
"""

from typing import List, Optional

from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import AnalyzeImageOptions, ImageData, ImageCategory
from azure.core.exceptions import HttpResponseError

from vision_client import get_azure_content_safety_client, load_image_bytes
from vision_models import SafetyCategory, SafetyResult, ImageAnalysisPayload


def score_image_safety(
    image_path: Optional[str] = None,
    image_bytes: Optional[bytes] = None,
    output_type: str = "FourSeverityLevels",
    blocklists: Optional[List[str]] = None,
) -> ImageAnalysisPayload:
    """
    Analyze an image for unsafe content using Azure Content Safety API.

    Evaluates the image across four harm categories: Hate, SelfHarm, Sexual, Violence.
    Each category receives a severity score from 0 to 7.

    Args:
        image_path: Path to the image file.
        image_bytes: Raw image bytes.
        output_type: Output format ('FourSeverityLevels' or 'EightSeverityLevels').
        blocklists: Optional list of blocklist names to check against.

    Returns:
        ImageAnalysisPayload containing safety results for each category.
    """
    raw_image = load_image_bytes(image_path=image_path, image_bytes=image_bytes)
    client = get_azure_content_safety_client()

    image_data = ImageData(content=raw_image)
    analyze_options = AnalyzeImageOptions(
        image=image_data,
        output_type=output_type,
    )

    if blocklists:
        analyze_options.blocklist_names = blocklists

    try:
        result = client.analyze_image(analyze_options)
    except HttpResponseError as e:
        return ImageAnalysisPayload(
            image_path=image_path,
            metadata={
                "provider": "azure_content_safety",
                "api_endpoint": "content-safety.cognitiveservices.azure.com",
                "error": str(e),
                "safety_check_failed": True,
            },
        )

    safety_results = []
    category_map = {
        ImageCategory.HATE: SafetyCategory.HATE,
        ImageCategory.SELF_HARM: SafetyCategory.SELF_HARM,
        ImageCategory.SEXUAL: SafetyCategory.SEXUAL,
        ImageCategory.VIOLENCE: SafetyCategory.VIOLENCE,
    }

    for category in ImageCategory:
        severity = result.categories_analysis.get(category, 0)
        safety_result = SafetyResult.from_azure_response(
            category_name=category.name,
            severity=severity,
        )
        safety_results.append(safety_result)

    payload = ImageAnalysisPayload(
        image_path=image_path,
        safety_results=safety_results,
        metadata={
            "provider": "azure_content_safety",
            "api_endpoint": "content-safety.cognitiveservices.azure.com",
            "output_type": output_type,
            "has_flags": any(r.is_flagged for r in safety_results),
            "max_severity": max(r.severity for r in safety_results) if safety_results else 0,
        },
    )

    return payload


def check_image_safe(
    image_path: Optional[str] = None,
    image_bytes: Optional[bytes] = None,
    severity_threshold: int = 4,
) -> bool:
    """
    Quick check if an image passes safety thresholds.

    Args:
        image_path: Path to the image file.
        image_bytes: Raw image bytes.
        severity_threshold: Maximum allowed severity (0-7 scale).

    Returns:
        True if image is safe (all categories below threshold).
    """
    payload = score_image_safety(
        image_path=image_path,
        image_bytes=image_bytes,
    )

    return all(
        r.severity < severity_threshold
        for r in payload.safety_results
    )


def get_safety_summary(
    payload: ImageAnalysisPayload,
) -> dict:
    """
    Generate a human-readable safety summary.

    Args:
        payload: ImageAnalysisPayload from score_image_safety.

    Returns:
        Dictionary with safety summary information.
    """
    summary = {
        "provider": "azure_content_safety",
        "is_safe": not payload.has_safety_flags(),
        "categories": {},
    }

    for result in payload.safety_results:
        summary["categories"][result.category.value] = {
            "severity": result.severity,
            "flagged": result.is_flagged,
        }

    return summary


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        result = score_image_safety(image_path=sys.argv[1])
        summary = get_safety_summary(result)
        print(f"Safe: {summary['is_safe']}")
        for cat, info in summary['categories'].items():
            print(f"  {cat}: severity={info['severity']}, flagged={info['flagged']}")
