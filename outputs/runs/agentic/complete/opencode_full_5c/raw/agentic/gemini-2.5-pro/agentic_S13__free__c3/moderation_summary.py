from safety_client import get_google_generativeai_client
from safety_models import ModerationSummaryRequest, ModerationSummaryResponse


def summarize_moderation_decisions(
    request: ModerationSummaryRequest,
) -> ModerationSummaryResponse:
    genai = get_google_generativeai_client()
    model = genai.GenerativeModel("gemini-1.5-flash")

    prompt = "Summarize the following moderation decisions:\n"
    for i, decision in enumerate(request.decisions):
        prompt += f"Item {i + 1}: Flagged={decision.flagged}, Categories={decision.categories}\n"

    response = model.generate_content(prompt)
    return ModerationSummaryResponse(summary=response.text)
