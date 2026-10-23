import os
from typing import Optional
from openai import OpenAI
from model_client import get_openai_client, select_text_model
from model_models import ChatPrompt, normalize_text_response


def summarize_text(text: str, max_sentences: int = 5, model: Optional[str] = None) -> str:
    client = get_openai_client()
    model_id = select_text_model(model=model, task="summarization")
    prompt = ChatPrompt(
        system="You are a concise summarization assistant.",
        user=f"Summarize the following text in at most {max_sentences} sentences:\n\n{text}",
    )
    response = client.chat.completions.create(
        model=model_id,
        messages=prompt.to_messages(),
        temperature=0.2,
    )
    return normalize_text_response(response)
