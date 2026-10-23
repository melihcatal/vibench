import os
from typing import Any, Dict, Optional

from openai import OpenAI


def localized_platform_output(text: str, target_locale: str, source_locale: Optional[str] = None) -> Dict[str, Any]:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    source = source_locale or "auto"
    prompt = (
        f"Translate the following platform model output from {source} to {target_locale}. "
        "Preserve meaning, formatting, labels, code, and structured data. Return only the translated text.\n\n"
        f"{text}"
    )
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt,
    )
    translated_text = response.output_text
    return {
        "translated_text": translated_text,
        "target_locale": target_locale,
        "source_locale": source_locale,
        "provider": "openai",
        "model": "gpt-4.1-mini",
        "response_id": getattr(response, "id", None),
    }
