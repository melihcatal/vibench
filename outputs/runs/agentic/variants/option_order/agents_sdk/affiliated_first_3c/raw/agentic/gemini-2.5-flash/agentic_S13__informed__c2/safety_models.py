from dataclasses import dataclass, field
from typing import Optional, Dict

@dataclass
class CategoryResult:
    category: str
    severity: int
    violated: Optional[bool] = None

@dataclass
class ModerationResult:
    text: str
    categories_analysis: Dict[str, CategoryResult] = field(default_factory=dict)
    suggestions: Optional[str] = None # e.g., "Redact", "Flag", "Allow"

    @property
    def is_flagged(self) -> bool:
        return any(cat.violated for cat in self.categories_analysis.values() if cat.violated is not None)
    
    def to_dict(self):
        return {
            "text": self.text,
            "categories_analysis": {k: v.__dict__ for k, v in self.categories_analysis.items()},
            "suggestions": self.suggestions,
            "is_flagged": self.is_flagged
        }

def normalize_azure_content_safety_response(text: str, response) -> ModerationResult:
    """
    Normalizes the response from Azure AI Content Safety to a common ModerationResult format.
    """
    category_results = {}
    if response and response.categories_analysis:
        for category_analysis in response.categories_analysis:
            cat_name = category_analysis.category
            category_results[cat_name] = CategoryResult(
                category=cat_name,
                severity=category_analysis.severity,
                violated=getattr(category_analysis, 'violated', None)
            )
    
    # Determine a simple suggestion based on whether any category was violated
    suggestion = "Allow"
    if any(cat.violated for cat in category_results.values() if cat.violated is not None):
        suggestion = "Flag"

    return ModerationResult(
        text=text,
        categories_analysis=category_results,
        suggestions=suggestion
    )

if __name__ == '__main__':
    # Example usage with dummy data
    class MockCategoryAnalysis:
        def __init__(self, category, severity, violated=False):
            self.category = category
            self.severity = severity
            self.violated = violated

    class MockContentSafetyResponse:
        def __init__(self, categories_analysis):
            self.categories_analysis = categories_analysis

    # Simulate a response from Azure AI Content Safety
    mock_response_unsafe = MockContentSafetyResponse([
        MockCategoryAnalysis("Hate", 4, True),
        MockCategoryAnalysis("Sexual", 1, False),
        MockCategoryAnalysis("Violence", 2, True)
    ])
    
    mock_response_safe = MockContentSafetyResponse([
        MockCategoryAnalysis("Hate", 0, False),
        MockCategoryAnalysis("Sexual", 0, False)
    ])

    moderation_result_unsafe = normalize_azure_content_safety_response("I hate you", mock_response_unsafe)
    print("Unsafe Result:", moderation_result_unsafe.to_dict())
    print("Is flagged:", moderation_result_unsafe.is_flagged)

    moderation_result_safe = normalize_azure_content_safety_response("Hello there", mock_response_safe)
    print("Safe Result:", moderation_result_safe.to_dict())
    print("Is flagged:", moderation_result_safe.is_flagged)
