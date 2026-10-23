import os
import google.generativeai as genai
from typing import List, Dict, Any
from safety_models import ModerationSummaryRequest, ModerationSummaryResult

def moderation_summary(request: ModerationSummaryRequest, config: Dict[str, Any] = None) -> ModerationSummaryResult:
    config = config or {}
    api_key = config.get("google_api_key") or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("Google API key not provided or found in environment variables.")

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro') # Concrete model identifier

    decision_strings = []
    for decision in request.moderation_decisions:
        decision_strings.append(f"Content: {decision.get("text", "N/A")}, Decision: {decision.get("overall_decision", "N/A")}, Reasons: {', '.join(decision.get("reasons", []))}, Scores: {decision.get("scores", "N/A")}")

    prompt = """Summarize the following moderation decisions. Highlight key issues and overall trends.

Moderation Decisions:
""" + "\n".join(decision_strings)

    response = model.generate_content(prompt)
    return ModerationSummaryResult(summary=response.text)
