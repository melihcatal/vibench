import os
from typing import Dict, Any, Optional

from safety_client import get_content_safety_client
from safety_models import ModerationRequest, RedactionResponse


def redact_unsafe(text: str, context: Dict[str, Any] = None) -> RedactionResponse:
    """
    Flags or redacts unsafe spans from text using Azure AI Content Safety.
    """
    client = get_content_safety_client()
    request = ModerationRequest(
        text=text,
        categories=["Hate", "Sexual", "Violence", "SelfHarm", "Harassment"],
        context=context or {},
    )

    try:
        response = client.analyze_text(
            text=text, categories=request.categories, output_type="FourSeverityLevels"
        )

        redacted_text = text
        offset = 0
        for result in response.get("categoryScores", []):
            if result["severity"] > 2:
                for location in result.get("locations", []):
                    start = location["offset"] + offset
                    end = start + location["length"]
                    redacted_text = (
                        redacted_text[:start] + "[REDACTED]" + redacted_text[end:]
                    )
                    offset += len("[REDACTED]") - location["length"]

        return RedactionResponse(
            original_text=text,
            redacted_text=redacted_text,
            unsafe_spans=[
                {
                    "start": loc["offset"],
                    "end": loc["offset"] + loc["length"],
                    "category": result["category"],
                }
                for result in response.get("categoryScores", [])
                for loc in result.get("locations", [])
                if result["severity"] > 2
            ],
        )
    except Exception as e:
        raise Exception(f"Azure AI Content Safety redaction failed: {str(e)}")
