import os
from typing import List

from openai import OpenAI


def check_unsafe_copy(text: str, locale: str, model: str = "gpt-4.1-mini") -> List[str]:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")
    client = OpenAI(api_key=api_key)
    prompt = f"Analyze this localized copy for unsafe content, including self-harm, hate, sexual content involving minors, threats, or illegal instructions. Return a JSON array of issue labels only. Locale: {locale}. Text: {text}"
    response = client.responses.create(model=model, input=prompt)
    try:
        import json
        return [str(item) for item in json.loads(response.output_text)]
    except Exception:
        return [response.output_text]
