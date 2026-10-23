import os
import google.generativeai as genai
from safety_models import ModerationSummaryRequest, ModerationSummaryResponse

def summarize_moderation_decisions(request: ModerationSummaryRequest) -> ModerationSummaryResponse:
    """
    Summarizes moderation decisions using Google Cloud Generative AI (Gemini).
    """
    # Configure Google Generative AI
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

    # Use a specific model, e.g., 'gemini-pro'
    model = genai.GenerativeModel('gemini-pro')

    decision_strings = []
    for decision in request.decisions:
        reasons = ", ".join(decision.reasons) if decision.reasons else "No specific reasons."
        decision_strings.append(f"Text: \"{decision.text}\", Decision: {decision.decision}, Reasons: {reasons}")

    prompt = (
        "Summarize the following moderation decisions. Highlight any patterns, common reasons for flagging/blocking, "
        "and the overall sentiment regarding the safety of the content. \n\n"
        + "\n".join(decision_strings)
    )

    try:
        response = model.generate_content(prompt)
        summary_text = response.text
    except Exception as e:
        summary_text = f"Error generating summary: {e}. Decisions: {decision_strings}"

    return ModerationSummaryResponse(summary=summary_text)
