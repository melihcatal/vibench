import os
from typing import List

from openai import OpenAI

OPENAI_API_KEY_ENV = "OPENAI_API_KEY"
OPENAI_MODEL_ENV = "OPENAI_MODEL"
DEFAULT_OPENAI_MODEL = "gpt-4o-mini"


def check_visual_labels_for_unsafe_text(labels: List[str]) -> bool:
    api_key = os.environ.get(OPENAI_API_KEY_ENV, "").strip()
    if not api_key:
        raise ValueError("OPENAI_API_KEY is required")
    model = os.environ.get(OPENAI_MODEL_ENV, DEFAULT_OPENAI_MODEL)
    client = OpenAI(api_key=api_key)
    prompt = "Determine whether any of the following visual labels contain unsafe, hateful, sexual, violent, or self-harm related text. Reply with only true or false. Labels: " + ", ".join(labels)
    response = client.responses.create(model=model, input=prompt)
    output = (response.output_text or "false").strip().lower()
    return output.startswith("true")
