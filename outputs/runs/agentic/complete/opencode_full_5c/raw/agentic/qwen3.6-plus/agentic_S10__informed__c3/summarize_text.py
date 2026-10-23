from typing import Optional
from model_client import create_chat_completion, get_openai_client
from model_models import LLMRequest, LLMResponse


def summarize_text(
    text: str,
    max_words: int = 150,
    model: str = "gpt-4o",
    api_key: Optional[str] = None,
) -> LLMResponse:
    client = get_openai_client(api_key) if api_key else None
    request = LLMRequest(
        prompt=text,
        model=model,
        temperature=0.3,
        max_tokens=512,
        system_prompt=(
            "You are a professional summarizer. "
            f"Provide a concise summary of the following text in no more than {max_words} words. "
            "Preserve key facts, names, and conclusions."
        ),
    )
    return create_chat_completion(request, client)
