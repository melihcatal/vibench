import os
from typing import Any, Dict, List

from openai import OpenAI


def translate_log_messages(messages: List[str], target_locale: str) -> Dict[str, Any]:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    prompt = {
        "role": "user",
        "content": (
            "Translate the following support-visible log messages into the target locale. "
            "Preserve meaning, identifiers, placeholders, timestamps, codes, and any technical tokens. "
            "Return JSON with a 'translations' array in the same order as the input messages. "
            f"Target locale: {target_locale}. Messages: {messages}"
        ),
    }
    response = client.responses.create(
        model="gpt-5-mini",
        input=[prompt],
        temperature=0,
    )
    text = response.output_text
    return {
        "target_locale": target_locale,
        "input_messages": messages,
        "response_text": text,
    }
