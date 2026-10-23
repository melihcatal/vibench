from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any

@dataclass
class ModerationCategory:
    """Represents a moderation category with its name and score/severity."""
    category: str
    score: Optional[float] = None  # Confidence score (e.g., from Google Cloud NL)
    severity: Optional[int] = None # Severity level (e.g., from Azure Content Safety)
    violated: Optional[bool] = None # Whether this category was explicitly violated by the service

@dataclass
class ModerationResult:
    """Standardized moderation result for a single piece of text."""
    input_text: str
    categories: List[ModerationCategory] = field(default_factory=list)
    overall_decision: str = "PENDING" # ALLOW, DENY, REVIEW
    reasons: List[str] = field(default_factory=list)
    raw_provider_response: Optional[Dict[str, Any]] = None

def normalize_google_nl_response(text: str, response: Any) -> ModerationResult:
    """Normalizes Google Cloud Natural Language API moderate_text response."""
    categories = []
    if response and hasattr(response, 'moderation_categories'):
        for cat in response.moderation_categories:
            categories.append(ModerationCategory(category=cat.name, score=cat.confidence))
    
    # Initial decision logic (can be refined by safety_threshold.py)
    overall_decision = "ALLOW"
    for cat in categories:
        if cat.score and cat.score > 0.7: # Example threshold
            overall_decision = "REVIEW"
            break

    return ModerationResult(
        input_text=text,
        categories=categories,
        overall_decision=overall_decision,
        raw_provider_response=response._pb # Store raw protobuf for debugging if needed
    )

def normalize_azure_cs_response(text: str, response: Any) -> ModerationResult:
    """Normalizes Azure Content Safety API analyze_text response."""
    categories = []
    if response and hasattr(response, 'categories_analysis'):
        for cat_analysis in response.categories_analysis:
            categories.append(ModerationCategory(
                category=cat_analysis.category.value,
                severity=cat_analysis.severity,
                violated=cat_analysis.violated
            ))

    # Initial decision logic (can be refined by safety_threshold.py)
    overall_decision = "ALLOW"
    for cat in categories:
        if cat.violated:
            overall_decision = "DENY"
            break
        if cat.severity and cat.severity >= 4: # Example severity threshold
            overall_decision = "REVIEW"
            break

    return ModerationResult(
        input_text=text,
        categories=categories,
        overall_decision=overall_decision,
        raw_provider_response=response.as_dict() # Store raw dictionary response
    )

# You can add more normalization functions for other providers here.

if __name__ == '__main__':
    # Example usage for normalization
    # This part would typically be used in the actual integration files (moderate_text.py, moderate_batch.py)
    
    # Mock Google NL response
    class MockGoogleNLModerationCategory:
        def __init__(self, name, confidence):
            self.name = name
            self.confidence = confidence

    class MockGoogleNLResponse:
        def __init__(self, categories):
            self.moderation_categories = categories
            self._pb = {"mock_pb_data": "GoogleNL"}

    mock_gcp_response = MockGoogleNLResponse([
        MockGoogleNLModerationCategory("TOXICITY", 0.95),
        MockGoogleNLModerationCategory("FLIRTATION", 0.2),
    ])
    normalized_gcp = normalize_google_nl_response("You are terrible!", mock_gcp_response)
    print("Normalized Google NL Response:", normalized_gcp)

    # Mock Azure CS response
    from azure.ai.contentsafety.models import TextCategory
    class MockAzureCSCategoryAnalysis:
        def __init__(self, category, severity, violated):
            self.category = category
            self.severity = severity
            self.violated = violated

    class MockAzureCSResponse:
        def __init__(self, categories_analysis):
            self.categories_analysis = categories_analysis
        
        def as_dict(self):
            return {"mock_dict_data": "AzureCS"}

    mock_azure_response = MockAzureCSResponse([
        MockAzureCSCategoryAnalysis(TextCategory.HATE, 4, True),
        MockAzureCSCategoryAnalysis(TextCategory.VIOLENCE, 1, False),
    ])
    normalized_azure = normalize_azure_cs_response("I hate you!", mock_azure_response)
    print("\nNormalized Azure CS Response:", normalized_azure)
