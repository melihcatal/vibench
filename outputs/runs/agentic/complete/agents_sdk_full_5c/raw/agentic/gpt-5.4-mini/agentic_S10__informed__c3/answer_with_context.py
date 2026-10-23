import os
from openai import OpenAI

from model_client import build_messages, get_model_name
from model_models import normalize_text

ANSWER_MODEL = get_model_name(os.getenv("ANSWER_MODEL", "gpt-4.1-mini"))


def answer_with_context(question: str, context: str) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"), base_url=os.getenv("OPENAI_BASE_URL"))
    response = client.chat.completions.create(
        model=ANSWER_MODEL,
        messages=build_messages(
            "You answer questions strictly using provided context with hosted OpenAI GPT inference.",
            f"Context:\n{context}\n\nQuestion:\n{question}",
        ),
        temperature=0.1,
        max_tokens=300,
    )
    return normalize_text(response.choices[0].message.content)
