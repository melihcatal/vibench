import os
from typing import Any, Dict, Optional

from openai import OpenAI


def localized_platform_output(text: str, locale: str, model: Optional[str] = None) -> Dict[str, Any]:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.responses.create(
        model=model or os.environ.get("OPENAI_MODEL", "gpt-4.1-mini"),
        input=[
            {
                "role": "system",
                "content": f"Translate the given platform model output into {locale}. Preserve meaning, tone, formatting, and any identifiers.",
            },
            {"role": "user", "content": text},
        ],
    )
    return {
        "locale": locale,
        "model": getattr(response, "model", model or os.environ.get("OPENAI_MODEL", "gpt-4.1-mini")),
        "output": response.output_text,
        "response": response,
    }
