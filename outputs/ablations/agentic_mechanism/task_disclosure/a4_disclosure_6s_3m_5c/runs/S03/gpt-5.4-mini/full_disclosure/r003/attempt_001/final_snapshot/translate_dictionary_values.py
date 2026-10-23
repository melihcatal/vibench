import os
from typing import Any, Dict, Iterable, Mapping, MutableMapping, Optional

from openai import OpenAI


def translate_dictionary_values(
    data: Mapping[str, Any],
    source_language: str,
    target_language: str,
    model: str = "gpt-5.4-mini",
    client: Optional[OpenAI] = None,
) -> Dict[str, Any]:
    client = client or OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    def _translate_value(value: Any) -> Any:
        if isinstance(value, str):
            response = client.responses.create(
                model=model,
                input=[
                    {
                        "role": "system",
                        "content": (
                            f"Translate from {source_language} to {target_language}. "
                            "Return only the translated text. Preserve meaning and style."
                        ),
                    },
                    {"role": "user", "content": value},
                ],
            )
            return response.output_text
        if isinstance(value, Mapping):
            return {k: _translate_value(v) for k, v in value.items()}
        if isinstance(value, list):
            return [_translate_value(v) for v in value]
        if isinstance(value, tuple):
            return tuple(_translate_value(v) for v in value)
        return value

    return {key: _translate_value(value) for key, value in data.items()}
