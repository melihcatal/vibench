import os
import google.generativeai as genai
from safety_models import ModerationDecision
from typing import List


def summarize_moderation_decisions(decisions: List[ModerationDecision]) -> str:
    google_api_key = os.environ.get("GOOGLE_API_KEY")
    if not google_api_key:
        raise ValueError("GOOGLE_API_KEY environment variable must be set.")

    genai.configure(api_key=google_api_key)

    model = genai.GenerativeModel("gemini-pro")  # Using gemini-pro for summarization

    decision_strings = []
    for decision in decisions:
        decision_strings.append(
            f"Text: '{decision.text}' - Decision: {decision.decision} - Reasons: {', '.join(decision.reasons)}"
        )

    prompt = "Summarize the following moderation decisions:\n" + "\n".join(
        decision_strings
    )

    response = model.generate_content(prompt)
    return response.text
