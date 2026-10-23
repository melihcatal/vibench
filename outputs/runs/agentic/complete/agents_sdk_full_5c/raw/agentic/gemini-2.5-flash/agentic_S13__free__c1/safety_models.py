from typing import List, Dict, Any, Optional
from dataclasses import dataclass

@dataclass
class ModerationCategoryScore:
    category: str
    score: float
    severity: Optional[int] = None # Google Cloud AI Platform sometimes returns severity levels

@dataclass
class UnifiedModerationResult:
    text: str
    is_allowed: bool
    reasons_for_denial: List[str]
    provider_specific_results: Dict[str, Any] # e.g., raw response from Google Cloud AI Platform
    safety_scores: List[ModerationCategoryScore]

def normalize_aiplatform_moderation_response(text: str, aiplatform_response: Any) -> UnifiedModerationResult:
    """
    Normalizes the response from Google Cloud AI Platform's generative model (text-bison)
    into a unified moderation result structure.
    This function parses the safety attributes typically found in `aiplatform_response.candidates[0].safety_attributes`.

    Args:
        text: The original text that was moderated.
        aiplatform_response: The raw response object from `aiplatform.get_model().predict()`.

    Returns:
        A UnifiedModerationResult object.
    """
    is_allowed = True
    reasons_for_denial = []
    safety_scores = []

    # The actual structure of safety attributes can vary. This is a common pattern.
    # For text-bison@001, safety attributes are usually part of `predictions` or `safetyAttributes`.
    # This part needs to be adapted based on the exact output format.

    # Simulate parsing based on expected GenAI safety output structure (placeholder)
    # In a real scenario, you'd access `aiplatform_response.candidates[0].safety_attributes`
    # or similar fields if they exist and are populated.

    # For the purpose of this example, let's assume the raw response contains a dictionary
    # under `predictions` with keys like 'harm_category_scores'.
    if hasattr(aiplatform_response, 'predictions') and isinstance(aiplatform_response.predictions, list):
        for prediction in aiplatform_response.predictions:
            # Assuming a structure like {'safetyAttributes': {'categories': [...], 'scores': [...]}}
            if 'safetyAttributes' in prediction and 'categories' in prediction['safetyAttributes'] and 'scores' in prediction['safetyAttributes']:
                categories = prediction['safetyAttributes']['categories']
                scores = prediction['safetyAttributes']['scores']
                severities = prediction['safetyAttributes'].get('severities', [None] * len(categories))

                for i, category in enumerate(categories):
                    score = scores[i] if i < len(scores) else 0.0
                    severity = severities[i] if i < len(severities) else None
                    safety_scores.append(ModerationCategoryScore(category=category, score=score, severity=severity))
                    # Example of applying a simple threshold within normalization
                    if category.startswith("HARM_CATEGORY_") and score > 0.7: # Example threshold
                        is_allowed = False
                        reasons_for_denial.append(f"High score ({score:.2f}) for {category}.")
    elif hasattr(aiplatform_response, 'candidates') and aiplatform_response.candidates:
        # Accessing safety ratings directly from candidate if available
        # This often looks like candidate.safety_ratings for models like gemini
        for candidate in aiplatform_response.candidates:
            if hasattr(candidate, 'safety_ratings'):
                for rating in candidate.safety_ratings:
                    category = rating.category.name if hasattr(rating.category, 'name') else str(rating.category)
                    score_value = rating.probability_score if hasattr(rating, 'probability_score') else 0.0
                    severity_value = rating.severity_score if hasattr(rating, 'severity_score') else None
                    safety_scores.append(ModerationCategoryScore(category=category, score=score_value, severity=severity_value))

                    # Apply a basic blocking logic if any category is high
                    if rating.probability >= aiplatform.genai.HarmProbability.HIGH: # Example for Gemini
                        is_allowed = False
                        reasons_for_denial.append(f"Content is {rating.probability.name} for {category}.")


    return UnifiedModerationResult(
        text=text,
        is_allowed=is_allowed,
        reasons_for_denial=list(set(reasons_for_denial)), # Remove duplicates
        provider_specific_results=aiplatform_response, # Store the raw response
        safety_scores=safety_scores
    )


@dataclass
class RedactionResult:
    original_text: str
    redacted_text: str
    detections: List[Dict[str, Any]] # e.g., info types detected by DLP


if __name__ == "__main__":
    # Example of a mock AI Platform response for testing normalization
    class MockSafetyRating:
        def __init__(self, category, probability, probability_score, severity_score):
            self.category = category
            self.probability = probability
            self.probability_score = probability_score
            self.severity_score = severity_score

    class MockCandidate:
        def __init__(self, text, safety_ratings):
            self.text = text
            self.safety_ratings = safety_ratings

    class MockAIPlatformResponse:
        def __init__(self, candidates):
            self.candidates = candidates
            self.predictions = [] # Mock for older models if needed

    # Define some mock harm probabilities if not available in the test environment
    class MockHarmProbability:
        UNSPECIFIED = 0
        BLOCKED = 1
        LOW = 2
        MEDIUM = 3
        HIGH = 4

        def __init__(self, name):
            self.name = name

    # Mock AI Platform HarmCategory
    class MockHarmCategory:
        UNSPECIFIED = 0
        HARM_CATEGORY_HATE_SPEECH = 1
        HARM_CATEGORY_DANGEROUS_CONTENT = 2
        HARM_CATEGORY_HARASSMENT = 3
        HARM_CATEGORY_SEXUALLY_EXPLICIT = 4

        def __init__(self, name):
            self.name = name


    mock_aiplatform_response_safe = MockAIPlatformResponse(
        candidates=[
            MockCandidate(
                text="This is a very safe response.",
                safety_ratings=[
                    MockSafetyRating(MockHarmCategory("HARM_CATEGORY_HATE_SPEECH"), MockHarmProbability("LOW"), 0.1, 0),
                    MockSafetyRating(MockHarmCategory("HARM_CATEGORY_DANGEROUS_CONTENT"), MockHarmProbability("LOW"), 0.05, 0),
                ]
            )
        ]
    )

    mock_aiplatform_response_unsafe = MockAIPlatformResponse(
        candidates=[
            MockCandidate(
                text="I will harm you with violence!",
                safety_ratings=[
                    MockSafetyRating(MockHarmCategory("HARM_CATEGORY_HATE_SPEECH"), MockHarmProbability("MEDIUM"), 0.6, 1),
                    MockSafetyRating(MockHarmCategory("HARM_CATEGORY_DANGEROUS_CONTENT"), MockHarmProbability("HIGH"), 0.9, 3),
                ]
            )
        ]
    )

    normalized_safe = normalize_aiplatform_moderation_response("Safe text query.", mock_aiplatform_response_safe)
    print("Normalized Safe Result:", normalized_safe)

    normalized_unsafe = normalize_aiplatform_moderation_response("Unsafe text query.", mock_aiplatform_response_unsafe)
    print("Normalized Unsafe Result:", normalized_unsafe)

