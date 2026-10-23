from model_client import complete_chat
from model_models import LLMRequest

SUMMARY_MODEL = "gpt-4o-mini"


def summarize_text(long_text: str) -> str:
    request = LLMRequest(
        prompt="Summarize the following text concisely and faithfully.",
        context=long_text,
        system="You are a helpful summarization assistant.",
        model=SUMMARY_MODEL,
        temperature=0.1,
        max_tokens=300,
    )
    return complete_chat(request).text
