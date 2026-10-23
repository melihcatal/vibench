from typing import List, Dict, Optional
from dataclasses import dataclass

@dataclass
class SafetyCategoryResult:
    category: str
    severity: int
    blocked: bool = False

@dataclass
class ModerationResult:
    text: str
    categories_analysis: Dict[str, SafetyCategoryResult]
    overall_blocked: bool = False
    overall_reasons: Optional[List[str]] = None

    @classmethod
    def from_azure_content_safety_response(cls, text: str, response_obj, custom_thresholds: Dict[str, int] = None):
        """
        Normalizes an Azure AI Content Safety `analyze_text` response into a common ModerationResult.
        """
        if custom_thresholds is None:
            custom_thresholds = { # Default example thresholds
                "hate": 4,
                "self_harm": 4,
                "sexual": 4,
                "violence": 4
            }

        category_results = {}
        overall_blocked = False
        overall_reasons = []

        for category_analysis in response_obj.categories_analysis:
            category_name = category_analysis.category.value.lower()
            severity = category_analysis.severity
            threshold = custom_thresholds.get(category_name, 999) # Use a very high threshold if not specified
            blocked_by_category = severity >= threshold

            category_results[category_name] = SafetyCategoryResult(
                category=category_name,
                severity=severity,
                blocked=blocked_by_category
            )

            if blocked_by_category:
                overall_blocked = True
                overall_reasons.append(f"Category '{category_name}' exceeded threshold (severity: {severity}, threshold: {threshold})")

        return cls(
            text=text,
            categories_analysis=category_results,
            overall_blocked=overall_blocked,
            overall_reasons=overall_reasons if overall_reasons else None
        )

@dataclass
class RedactionResult:
    original_text: str
    redacted_text: str
    unsafe_spans_detected: List[Dict]
    redaction_applied: bool

if __name__ == '__main__':
    # Example usage (mocking a response)
    class MockCategoryAnalysis:
        def __init__(self, category_value, severity):
            self.category = type('Category', (object,), {'value': category_value})()
            self.severity = severity

    class MockAnalyzeTextResponse:
        def __init__(self, categories_analysis):
            self.categories_analysis = categories_analysis

    mock_response = MockAnalyzeTextResponse([
        MockCategoryAnalysis("Hate", 3),
        MockCategoryAnalysis("Sexual", 5), # This will block
        MockCategoryAnalysis("Violence", 1)
    ])

    moderation_output = ModerationResult.from_azure_content_safety_response(
        text="This is some text.",
        response_obj=mock_response,
        custom_thresholds={
            "hate": 4,
            "sexual": 4,
            "violence": 2
        }
    )

    # print(moderation_output)
    # print(moderation_output.overall_blocked)
    # print(moderation_output.overall_reasons)
    pass
