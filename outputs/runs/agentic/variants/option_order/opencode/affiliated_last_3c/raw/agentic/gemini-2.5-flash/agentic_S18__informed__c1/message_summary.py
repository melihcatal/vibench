from messaging_client import get_gemini_client
from messaging_models import MessageSummaryRequest


def summarize_message(request: MessageSummaryRequest) -> str:
    model = get_gemini_client()
    response = model.generate_content(
        f"Summarize the following message content concisely: {request.message_content}"
    )
    return response.text
