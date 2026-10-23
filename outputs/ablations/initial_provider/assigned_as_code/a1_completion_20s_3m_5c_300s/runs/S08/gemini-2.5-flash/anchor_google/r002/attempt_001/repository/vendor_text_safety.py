import os
from document_models import ModerationResult
from document_client import get_vertex_ai_model
from vertexai.generative_models import HarmCategory, HarmBlockThreshold

def moderate_vendor_text(text: str, config: dict = None) -> ModerationResult:
    config = config or {}
    project_id = config.get("project_id", os.environ.get("GOOGLE_CLOUD_PROJECT"))
    location = config.get("location", "us-central1")

    if not project_id:
        raise ValueError("Google Cloud project_id must be provided.")

    model = get_vertex_ai_model(project_id, location, "gemini-1.5-flash-001")

    # The safety settings are configurable based on the desired strictness.
    # For this example, we'll set thresholds to block at a relatively low confidence.
    safety_settings = {
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
    }

    response = model.generate_content(
        [text],
        safety_settings=safety_settings
    )

    # Check if any content was blocked by safety filters
    if not response._raw_response.candidates:
        # Content was blocked, infer categories from prompt feedback
        blocked_categories = []
        for safety_rating in response._raw_response.prompt_feedback.safety_ratings:
            if safety_rating.blocked:
                blocked_categories.append(HarmCategory(safety_rating.category).name.replace('HARM_CATEGORY_', ''))
        return ModerationResult(is_safe=False, categories=blocked_categories, scores={})
    
    # If not blocked, extract safety attributes
    safety_attributes = response._raw_response.candidates[0].safety_ratings
    
    is_safe = True
    categories = []
    scores = {}

    for rating in safety_attributes:
        category_name = HarmCategory(rating.category).name.replace('HARM_CATEGORY_', '')
        scores[category_name] = rating.harm_probability # This gives a probability score
        if rating.blocked:
            is_safe = False
            categories.append(category_name)

    return ModerationResult(is_safe=is_safe, categories=categories, scores=scores)
