import os
from openai import OpenAI

from model_client import build_messages, get_model_name
from model_models import normalize_text

SUMMARY_MODEL = get_model_name(os.getenv("SUMMARIZE_MODEL", "gpt-4.1-mini"))


def summarize_text(long_text: str, max_tokens: int = 220) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"), base_url=os.getenv("OPENAI_BASE_URL"))
    response = client.chat.completions.create(
        model=SUMMARY_MODEL,
        messages=build_messages(
            "You are a concise summarization assistant for hosted OpenAI GPT inference.",
            f"Summarize the following text in a clear paragraph:\n\n{long_text}",
        ),
        temperature=0.2,
        max_tokens=max_tokens,
    )
    return normalize_text(response.choices[0].message.content)
