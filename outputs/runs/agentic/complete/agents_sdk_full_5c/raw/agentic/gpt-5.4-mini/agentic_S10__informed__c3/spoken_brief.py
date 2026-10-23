import os
from openai import OpenAI

from model_client import build_messages, get_model_name
from model_models import normalize_text

TTS_BRIEF_MODEL = get_model_name(os.getenv("TTS_BRIEF_MODEL", "gpt-4.1-mini"))


def generate_spoken_brief(model_output: str) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"), base_url=os.getenv("OPENAI_BASE_URL"))
    response = client.chat.completions.create(
        model=TTS_BRIEF_MODEL,
        messages=build_messages(
            "You convert model output into a short spoken brief using hosted OpenAI GPT inference.",
            f"Rewrite the following for spoken delivery in under 90 words:\n\n{model_output}",
        ),
        temperature=0.2,
        max_tokens=160,
    )
    return normalize_text(response.choices[0].message.content)
