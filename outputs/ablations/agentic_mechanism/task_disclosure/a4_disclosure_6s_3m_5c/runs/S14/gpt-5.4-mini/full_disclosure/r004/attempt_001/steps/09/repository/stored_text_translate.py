import json
import os
from typing import Any, Dict, Optional

import requests


OPENAI_CHAT_COMPLETIONS_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-4o-mini"


def _load_text(source: Any) -> str:
    if source is None:
        raise ValueError("source is required")
    if isinstance(source, str):
        if os.path.exists(source):
            with open(source, "r", encoding="utf-8") as f:
                return f.read()
        return source
    if hasattr(source, "read"):
        data = source.read()
        if isinstance(data, bytes):
            return data.decode("utf-8")
        return str(data)
    raise TypeError("unsupported source type")


def translate_text_extracted_from_stored_document(
    source: Any,
    target_language: str,
    api_key: Optional[str] = None,
    model: str = OPENAI_MODEL,
) -> Dict[str, Any]:
    api_key = api_key or os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is required")
    if not target_language:
        raise ValueError("target_language is required")
    text = _load_text(source)
    response = requests.post(
        OPENAI_CHAT_COMPLETIONS_URL,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json={
            "model": model,
            "messages": [
                {"role": "system", "content": "Translate the user's text accurately and preserve meaning, formatting, and line breaks when possible."},
                {"role": "user", "content": f"Translate the following text into {target_language}:\n\n{text}"},
            ],
            "temperature": 0,
        },
        timeout=120,
    )
    response.raise_for_status()
    data = response.json()
    translated_text = data["choices"][0]["message"]["content"]
    return {"translated_text": translated_text, "model": model, "raw": data}


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("source")
    parser.add_argument("target_language")
    parser.add_argument("--api-key")
    parser.add_argument("--model", default=OPENAI_MODEL)
    args = parser.parse_args()
    result = translate_text_extracted_from_stored_document(
        args.source,
        args.target_language,
        api_key=args.api_key,
        model=args.model,
    )
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
