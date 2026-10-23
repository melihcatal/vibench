import os
from typing import List, Optional

import openai


def translate_consent_copy(text: str, target_language: str, source_language: str = "en") -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    client = openai.OpenAI(api_key=api_key)
    response = client.responses.create(
        model="gpt-5.4-mini",
        input=[
            {
                "role": "system",
                "content": "You translate identity-provider consent copy accurately, preserving legal and security meaning.",
            },
            {
                "role": "user",
                "content": f"Translate from {source_language} to {target_language}: {text}",
            },
        ],
    )

    output_text = getattr(response, "output_text", None)
    if output_text:
        return output_text.strip()

    chunks: List[str] = []
    for item in response.output:
        for content in getattr(item, "content", []):
            value = getattr(content, "text", None)
            if value:
                chunks.append(value)
    if not chunks:
        raise RuntimeError("No translation returned")
    return "".join(chunks).strip()


def main() -> None:
    import sys

    if len(sys.argv) < 3:
        raise SystemExit("usage: consent_translate.py TARGET_LANGUAGE TEXT [SOURCE_LANGUAGE]")
    target_language = sys.argv[1]
    text = sys.argv[2]
    source_language = sys.argv[3] if len(sys.argv) > 3 else "en"
    print(translate_consent_copy(text=text, target_language=target_language, source_language=source_language))


if __name__ == "__main__":
    main()
