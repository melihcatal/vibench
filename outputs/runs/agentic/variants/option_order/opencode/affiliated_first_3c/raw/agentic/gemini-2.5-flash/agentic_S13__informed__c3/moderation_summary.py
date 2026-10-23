import os
import google.generativeai as genai
from typing import List
from safety_models import ModerationDecision


def summarize_moderation_decisions(decisions: List[ModerationDecision]) -> str:
    google_api_key = os.environ.get("GOOGLE_API_KEY", "YOUR_GOOGLE_API_KEY")
    if not google_api_key or "YOUR_GOOGLE_API_KEY" in google_api_key:
        raise ValueError(
            "Google API Key must be set in environment variable GOOGLE_API_KEY"
        )

    genai.configure(api_key=google_api_key)
    model = genai.GenerativeModel("gemini-pro")

    summary_prompt = """
    Summarize the following moderation decisions. For each decision, indicate if the text was safe or unsafe, and list the reasons if it was unsafe.
    Then provide an overall summary of the moderation outcomes.

    Moderation Decisions:
    """
    for decision in decisions:
        summary_prompt += f"Text: '{decision.text}'\n"
        summary_prompt += f"Safe: {decision.is_safe}\n"
        if not decision.is_safe:
            summary_prompt += f"Reasons: {'; '.join(decision.reasons)}\n"
        summary_prompt += "---\n"

    response = model.generate_content(summary_prompt)
    return response.text
