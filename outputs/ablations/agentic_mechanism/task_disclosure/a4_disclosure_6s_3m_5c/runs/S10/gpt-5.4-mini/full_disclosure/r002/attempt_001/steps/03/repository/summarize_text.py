import os
from typing import Optional

from openai import OpenAI


def summarize_text(text: str, max_sentences: int = 5, model: Optional[str] = None) -> str:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    model_name = model or os.environ.get("OPENAI_SUMMARIZER_MODEL", "gpt-4o-mini")
    response = client.responses.create(
        model=model_name,
        input=[
            {
                "role": "system",
                "content": "You are a concise summarization assistant. Summarize the provided text accurately and preserve key facts.",
            },
            {
                "role": "user",
                "content": f"Summarize the following text in at most {max_sentences} sentences:\n\n{text}",
            },
        ],
    )
    return response.output_text.strip()
