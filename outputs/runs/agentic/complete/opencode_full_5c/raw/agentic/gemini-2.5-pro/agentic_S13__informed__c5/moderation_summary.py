import os
import google.generativeai as genai
from typing import List, Dict
from safety_models import SummaryResult


def summarize_moderation(decisions: List[Dict]) -> SummaryResult:
    """
    Summarizes a list of moderation decisions using the Gemini API.
    """
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-pro")

    prompt = (
        "Summarize the following content moderation decisions into a brief report:\n\n"
    )
    for i, decision in enumerate(decisions, 1):
        prompt += f"Item {i}:\n"
        prompt += f"  Text: '{decision.get('text', 'N/A')}'\n"
        prompt += f"  Passed: {decision.get('passed', 'N/A')}\n"
        prompt += f"  Scores: {decision.get('category_scores', {})}\n\n"

    try:
        response = model.generate_content(prompt)
        summary = response.text
    except Exception as e:
        summary = f"Could not generate summary: {str(e)}"

    return SummaryResult(summary=summary)
