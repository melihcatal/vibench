from __future__ import annotations

from typing import Dict

from model_client import OPENAI_DEFAULT_MODEL, get_openai_client
from model_models import extract_text_from_response


def localized_platform_output(text: str, target_locale: str) -> Dict[str, str]:
    client = get_openai_client()
    response = client.responses.create(
        model=OPENAI_DEFAULT_MODEL,
        input=[
            {
                "role": "system",
                "content": f"Translate the user's text to locale {target_locale}.",
            },
            {"role": "user", "content": text},
        ],
        max_output_tokens=512,
    )
    return {
        "provider": "openai",
        "model": OPENAI_DEFAULT_MODEL,
        "locale": target_locale,
        "text": extract_text_from_response(response),
    }
