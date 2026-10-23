import os
import google.generativeai as genai
from safety_models import ModerationSummaryRequest, ModerationSummaryResponse


def moderation_summary(payload: ModerationSummaryRequest, config=None) -> ModerationSummaryResponse:
    config = config or {}
    genai.configure(api_key=config.get('GOOGLE_API_KEY', os.environ.get('GOOGLE_API_KEY')))
    model = genai.GenerativeModel('gemini-pro')

    decision_strings = []
    for decision in payload.decisions:
        decision_strings.append(f"Text: {decision.text}, Decision: {decision.decision}, Reasons: {', '.join(decision.reasons)}")

    prompt = f"Summarize the following moderation decisions:\n" + "\n".join(decision_strings)

    response = model.generate_content(prompt)
    return ModerationSummaryResponse(summary=response.text)
