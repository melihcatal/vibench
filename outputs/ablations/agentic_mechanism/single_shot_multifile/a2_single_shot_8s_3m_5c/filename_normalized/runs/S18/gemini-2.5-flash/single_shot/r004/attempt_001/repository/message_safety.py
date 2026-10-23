import os
from google.cloud import aiplatform
from messaging_models import SafetyCheckResult

def check_message_safety(text: str, project_id: str = None, region: str = None) -> SafetyCheckResult:
    if not project_id:
        project_id = os.environ.get("GCP_PROJECT_ID")
    if not region:
        region = os.environ.get("GCP_REGION", "us-central1")

    if not project_id:
        raise ValueError("GCP_PROJECT_ID environment variable or argument not set.")

    aiplatform.init(project=project_id, location=region)

    parameters = {
        "temperature": 0.2,
        "max_output_tokens": 256,
        "top_p": 0.95,
        "top_k": 40
    }

    model = aiplatform.preview.language_models.TextGenerationModel.from_pretrained("gemini-pro")

    # Vertex AI models automatically include safety attributes in responses
    response = model.predict(text, **parameters)

    safety_attributes = response.safety_attributes or {}
    blocked = safety_attributes.get('blocked', False)
    categories = safety_attributes.get('categories', [])
    scores = safety_attributes.get('scores', [])

    # Calculate an overall safety score if scores are provided, or use a default
    overall_score = sum(scores) / len(scores) if scores else 0.0

    # Determine if unsafe based on whether it was blocked or if any category score is high
    is_safe = not blocked and overall_score < 0.8 # Example threshold

    return SafetyCheckResult(
        is_safe=is_safe,
        categories=[{'category': c, 'score': s} for c, s in zip(categories, scores)],
        overall_score=overall_score
    )
