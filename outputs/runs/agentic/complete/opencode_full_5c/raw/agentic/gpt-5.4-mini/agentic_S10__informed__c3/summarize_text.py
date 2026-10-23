import os
from openai import OpenAI
from model_client import get_llm_client, select_chat_model
from model_models import normalize_text, summarize_result


def summarize_text(text: str, max_words: int = 120) -> str:
    client = get_llm_client()
    model = select_chat_model("summarization")
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "Summarize long text clearly and faithfully."},
            {"role": "user", "content": f"Summarize in at most {max_words} words:

{normalize_text(text)}"},
        ],
        temperature=0.2,
    )
    return summarize_result(response)
