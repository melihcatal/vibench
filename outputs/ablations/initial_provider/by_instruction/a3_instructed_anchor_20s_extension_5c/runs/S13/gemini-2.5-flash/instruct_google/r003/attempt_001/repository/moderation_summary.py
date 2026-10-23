import os
import vertexai
from typing import List
from safety_client import SafetyClient
from safety_models import ModerationResult
from vertexai.preview.generative_models import GenerativeModel

def summarize_moderation_decisions(results: List[ModerationResult]) -> str:
    """
    Summarizes moderation decisions for a list of ModerationResult objects using Google Vertex AI.
    """
    safety_client = SafetyClient()
    model = safety_client.get_generative_model("gemini-pro")

    summary_prompt = """Review the following moderation decisions and provide a concise summary of the overall outcome, highlighting any blocked content and the reasons. Also, suggest any actionable insights or common themes if present.

Moderation Results:
"""

    for result in results:
        summary_prompt += f"\n- Text: '{result.text}'\n  Allowed: {result.is_allowed}\n  Reasons: {', '.join(result.reasons) if result.reasons else 'N/A'}\n  Safety Ratings: {', '.join([f'{s.category}: {s.probability}' for s in result.safety_ratings]) if result.safety_ratings else 'N/A'}\n"

    response = model.generate_content([summary_prompt])

    return response.text
