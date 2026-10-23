from typing import Optional
from model_client import get_openai_client, select_text_model
from model_models import ChatPrompt, normalize_text_response


def result_translate(text: str, target_language: str, source_language: Optional[str] = None, model: Optional[str] = None) -> str:
    client = get_openai_client()
    model_id = select_text_model(model=model, task="translation")
    source_hint = f" from {source_language}" if source_language else ""
    prompt = ChatPrompt(
        system="You are a precise translation engine.",
        user=f"Translate the following text{source_hint} into {target_language}:\n\n{text}",
    )
    response = client.chat.completions.create(
        model=model_id,
        messages=prompt.to_messages(),
        temperature=0.1,
    )
    return normalize_text_response(response)
