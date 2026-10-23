import os
from typing import Dict, Any
from database_client import get_comprehend_client
from database_models import SafetyCheckRequest, SafetyCheckResponse


def record_text_safety(request: SafetyCheckRequest) -> SafetyCheckResponse:
    """
    Check user-generated document fields for unsafe content using Amazon Comprehend.
    """
    comprehend = get_comprehend_client()

    try:
        response = comprehend.detect_toxic_content(
            TextSegments=[{"Text": request.text}], LanguageCode=request.language_code
        )

        results = response["ResultList"][0]
        toxic_labels = []
        confidence_scores = {}

        for label in results["Labels"]:
            if label["Score"] > 0.5:
                toxic_labels.append(label["Name"])
                confidence_scores[label["Name"]] = label["Score"]

        is_safe = len(toxic_labels) == 0

        return SafetyCheckResponse(
            success=True,
            is_safe=is_safe,
            unsafe_categories=toxic_labels,
            confidence_scores=confidence_scores,
            message="Text safety check completed using Amazon Comprehend",
        )
    except Exception as e:
        return SafetyCheckResponse(
            success=False,
            is_safe=False,
            unsafe_categories=[],
            confidence_scores={},
            error_message=str(e),
            message="Failed to check text safety",
        )
