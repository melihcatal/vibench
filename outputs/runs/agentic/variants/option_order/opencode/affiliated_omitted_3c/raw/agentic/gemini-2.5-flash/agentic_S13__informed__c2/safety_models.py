from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class ModerationResult:
    category: str
    severity: int


@dataclass
class TextModerationResponse:
    text: str
    results: List[ModerationResult]


def parse_content_safety_response(
    raw_response: Dict[str, Any], text: str
) -> TextModerationResponse:
    """
    Parses the raw response from Azure AI Content Safety into a structured TextModerationResponse.
    """
    results = []
    if "categoriesAnalysis" in raw_response:
        for category_analysis in raw_response["categoriesAnalysis"]:
            results.append(
                ModerationResult(
                    category=category_analysis["category"],
                    severity=category_analysis["severity"],
                )
            )
    return TextModerationResponse(text=text, results=results)
