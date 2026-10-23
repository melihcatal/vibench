from safety_models import SummaryRequest, SummaryResponse
from safety_client import summarize_text_with_openai


def summarize_moderation_decisions(
    text_to_summarize: str, max_tokens: int = 100
) -> SummaryResponse:
    request = SummaryRequest(text=text_to_summarize, max_tokens=max_tokens)
    response = summarize_text_with_openai(request)
    return response
