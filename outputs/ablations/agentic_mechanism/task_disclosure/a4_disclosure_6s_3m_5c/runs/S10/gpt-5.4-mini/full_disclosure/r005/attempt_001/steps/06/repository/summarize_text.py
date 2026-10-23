import os
from typing import Optional

from openai import OpenAI


def summarize_text(text: str, max_sentences: int = 3, model: Optional[str] = None) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    model_id = model or os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
    prompt = f"Summarize the following text in at most {max_sentences} sentences. Focus on the key points and preserve important details.\n\n{text}"
    response = client.responses.create(
        model=model_id,
        input=[
            {
                "role": "system",
                "content": "You are a concise and accurate summarization assistant.",
            },
            {"role": "user", "content": prompt},
        ],
    )
    return response.output_text.strip()
