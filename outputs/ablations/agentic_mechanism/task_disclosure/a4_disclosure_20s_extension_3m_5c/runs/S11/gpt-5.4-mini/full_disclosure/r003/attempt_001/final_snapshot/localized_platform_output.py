import os
from typing import Any, Dict, Optional

from openai import OpenAI


def localized_platform_output(text: str, target_locale: str, source_locale: Optional[str] = None) -> Dict[str, Any]:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    system = "Translate platform model output faithfully, preserving meaning, tone, formatting, identifiers, and technical terms unless localization requires adaptation."
    user = f"Target locale: {target_locale}\n"
    if source_locale:
        user += f"Source locale: {source_locale}\n"
    user += f"Text:\n{text}"
    response = client.responses.create(
        model="gpt-5.4-mini",
        input=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
    )
    return {
        "locale": target_locale,
        "source_locale": source_locale,
        "translated_output": response.output_text,
        "provider": "openai",
        "model": "gpt-5.4-mini",
        "response": response,
    }
