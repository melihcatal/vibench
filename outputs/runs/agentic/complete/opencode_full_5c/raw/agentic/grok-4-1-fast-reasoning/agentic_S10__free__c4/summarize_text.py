from model_client import get_llm_client, get_model_id
from model_models import build_summarize_prompt, parse_chat_completion
from typing import Optional


def summarize_text(
    text: str, model_family: str = "gpt-4o-mini", max_tokens: Optional[int] = None
) -> str:
    client = get_llm_client()
    model = get_model_id(model_family)
    messages = build_summarize_prompt(text)
    kwargs = {"model": model, "messages": messages, "temperature": 0.3}
    if max_tokens:
        kwargs["max_tokens"] = max_tokens
    response = client.chat.completions.create(**kwargs)
    return parse_chat_completion(response)
