import os
from typing import Any, Dict, List, Optional

import requests


OPENAI_CHAT_COMPLETIONS_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_DEFAULT_MODEL = "gpt-4o-mini"


def _build_messages(text: str, source_language: Optional[str], target_language: Optional[str]) -> List[Dict[str, str]]:
    source = source_language or "auto-detected"
    target = target_language or "English"
    return [
        {
            "role": "system",
            "content": "You translate encryption and compliance notes for reviewers. Preserve technical meaning, identifiers, and security caveats.",
        },
        {
            "role": "user",
            "content": f"Translate the following note from {source} to {target}. Return only the translated note:\n\n{text}",
        },
    ]


def translate_compliance_note(text: str, source_language: Optional[str] = None, target_language: Optional[str] = None, model: Optional[str] = None, timeout: int = 30) -> str:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")
    payload = {
        "model": model or OPENAI_DEFAULT_MODEL,
        "messages": _build_messages(text, source_language, target_language),
        "temperature": 0,
    }
    response = requests.post(
        OPENAI_CHAT_COMPLETIONS_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=timeout,
    )
    response.raise_for_status()
    data: Dict[str, Any] = response.json()
    choices = data.get("choices") or []
    if not choices:
        raise RuntimeError("OpenAI response did not include any choices")
    message = choices[0].get("message") or {}
    content = message.get("content")
    if not isinstance(content, str) or not content.strip():
        raise RuntimeError("OpenAI response did not include translated content")
    return content.strip()


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Translate encryption or compliance notes for reviewers")
    parser.add_argument("text")
    parser.add_argument("--source-language")
    parser.add_argument("--target-language")
    parser.add_argument("--model")
    args = parser.parse_args()
    print(translate_compliance_note(args.text, args.source_language, args.target_language, args.model))


if __name__ == "__main__":
    main()
