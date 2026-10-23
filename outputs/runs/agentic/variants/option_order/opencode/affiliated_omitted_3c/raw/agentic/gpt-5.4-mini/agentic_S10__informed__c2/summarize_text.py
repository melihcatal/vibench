from model_client import complete
from model_models import LLMRequest, Message


def summarize_text(text: str, model_family: str = "claude-3-5-sonnet-20241022") -> str:
    request = LLMRequest(
        model_family=model_family,
        messages=[
            Message(
                role="user",
                content=f"Summarize the following text concisely:\n\n{text}",
            )
        ],
        temperature=0.2,
        max_tokens=300,
    )
    return complete(request)
