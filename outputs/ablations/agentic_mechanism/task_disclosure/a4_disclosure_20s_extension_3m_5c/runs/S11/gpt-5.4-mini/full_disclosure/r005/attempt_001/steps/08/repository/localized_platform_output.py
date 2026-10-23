import os
from typing import Any, Dict, Optional

from openai import OpenAI


def localized_platform_output(text: str, target_locale: str, source_locale: Optional[str] = None) -> Dict[str, Any]:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    prompt = (
        f"Translate the following platform model output into {target_locale}. "
        + (f"The source locale is {source_locale}. " if source_locale else "")
        + "Return only the translated text.\n\n"
        + text
    )
    response = client.responses.create(
        model="gpt-5.4-mini",
        input=prompt,
    )
    translated_text = getattr(response, "output_text", None)
    if translated_text is None:
        translated_text = ""
        for item in getattr(response, "output", []) or []:
            for content in getattr(item, "content", []) or []:
                value = getattr(content, "text", None)
                if value:
                    translated_text += value
    return {
        "translated_text": translated_text,
        "locale": target_locale,
        "provider": "openai",
        "model": "gpt-5.4-mini",
        "response": response,
    }
