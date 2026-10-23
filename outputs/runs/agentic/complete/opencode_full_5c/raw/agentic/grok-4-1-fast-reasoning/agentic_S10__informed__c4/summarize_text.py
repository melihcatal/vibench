from model_client import select_model_for_task, get_api_key
from model_models import build_prompt_for_summarize
import anthropic


def summarize_text(text: str) -> str:
    provider, model = select_model_for_task("summarize")
    api_key = get_api_key(provider)
    client = anthropic.Anthropic(api_key=api_key)
    messages = build_prompt_for_summarize(text)
    response = client.messages.create(
        model=model, max_tokens=1024, temperature=0.3, messages=messages
    )
    if isinstance(response.content, str):
        return response.content
    else:
        return "".join([block.text for block in response.content])
