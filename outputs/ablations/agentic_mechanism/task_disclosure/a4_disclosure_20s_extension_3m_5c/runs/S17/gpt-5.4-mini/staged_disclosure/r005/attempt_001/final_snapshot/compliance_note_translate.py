import os
from typing import Optional

import httpx


OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-4o-mini"


def translate_compliance_note(note: str, target_language: str = "English", source_language: Optional[str] = None) -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    system_prompt = "Translate encryption or compliance notes for reviewers. Preserve technical meaning, policy language, and any control references. Return only the translation."
    user_prompt = f"Translate this compliance note into {target_language}."
    if source_language:
        user_prompt += f" Source language: {source_language}."
    user_prompt += f"\n\nNote:\n{note}"

    response = httpx.post(
        OPENAI_API_URL,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json={
            "model": OPENAI_MODEL,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": 0,
        },
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"].strip()


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Translate encryption or compliance notes for reviewers using OpenAI.")
    parser.add_argument("note")
    parser.add_argument("--target-language", default="English")
    parser.add_argument("--source-language")
    args = parser.parse_args()
    print(translate_compliance_note(args.note, args.target_language, args.source_language))


if __name__ == "__main__":
    main()
