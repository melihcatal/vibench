import os
import google.generativeai as genai
from typing import List
from safety_models import ModerationDecision

def summarize_moderation_decisions(decisions: List[ModerationDecision], config=None) -> str:
    """
    Summarizes a list of moderation decisions using Google Gemini.

    Args:
        decisions: A list of ModerationDecision objects.
        config: Optional configuration dictionary, may contain 'api_key'.

    Returns:
        A summary string of the moderation decisions.
    """
    api_key = config.get("api_key") if config else None
    genai.configure(api_key=api_key or os.environ.get("GEMINI_API_KEY"))

    model = genai.GenerativeModel('gemini-pro')

    decision_texts = []
    for decision in decisions:
        decision_texts.append(f"Text: \"{decision.text}\", Decision: {decision.decision}, Reason: {decision.reason}")

    prompt = (
        "Summarize the following moderation decisions. Group similar decisions and highlight any critical issues.\n\n"
        + "\n".join(decision_texts)
        + "\n\nSummary:"
    )

    response = model.generate_content(prompt)
    return response.text
