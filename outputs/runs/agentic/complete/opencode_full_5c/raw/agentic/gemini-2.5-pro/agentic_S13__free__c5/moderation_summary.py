from typing import List
from safety_client import get_vertexai_client
from safety_models import ModerationDecision
from vertexai.generative_models import GenerativeModel


def summarize_moderation_decisions(decisions: List[ModerationDecision]) -> str:
    """
    Summarize moderation decisions using Google's Gemini model via Vertex AI.
    """
    get_vertexai_client()  # Initializes the client
    model = GenerativeModel("gemini-1.0-pro")

    prompt = "Summarize the following content moderation decisions:\n\n"
    for decision in decisions:
        prompt += f'- Text: "{decision.text[:50]}..."\n'
        prompt += f"  - Safe: {decision.is_safe}\n"
        if not decision.is_safe:
            prompt += f"  - Violations: {', '.join(decision.violations)}\n"

    prompt += "\nProvide a brief, high-level summary of these moderation actions."

    response = model.generate_content(prompt)
    return response.text
