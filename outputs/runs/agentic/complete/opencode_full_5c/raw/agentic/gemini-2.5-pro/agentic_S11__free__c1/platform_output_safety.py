from vertexai.generative_models import GenerateContentResponse
from vertexai.generative_models._generative_models import HarmCategory


def check_content_safety(response: GenerateContentResponse) -> bool:
    """
    Checks the safety ratings from a Vertex AI response.
    Returns True if the content is considered safe, False otherwise.
    """
    if not response.prompt_feedback:
        return True

    for rating in response.prompt_feedback.safety_ratings:
        if rating.severity.value > 1:  # Higher values indicate higher severity
            return False
    return True
