import os
from typing import Any, Dict, List, Optional

import openai


def _client() -> openai.OpenAI:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is required")
    return openai.OpenAI(api_key=api_key)


def summarize_translation_quality(
    source_text: str,
    translated_text: str,
    target_language: str,
    model: str = "gpt-5.4-mini",
) -> Dict[str, Any]:
    prompt = (
        "Analyze the translation quality and summarize issues. "
        "Return concise JSON with keys: overall_assessment, issues, severity, suggestions. "
        f"Source language content: {source_text}\n"
        f"Translated text ({target_language}): {translated_text}"
    )
    client = _client()
    response = client.responses.create(
        model=model,
        input=prompt,
        temperature=0,
    )
    output = getattr(response, "output_text", "") or ""
    return {"provider": "openai", "model": model, "summary": output}


def summarize_batch(
    items: List[Dict[str, str]],
    target_language: str,
    model: str = "gpt-5.4-mini",
) -> List[Dict[str, Any]]:
    return [
        summarize_translation_quality(
            source_text=item.get("source_text", ""),
            translated_text=item.get("translated_text", ""),
            target_language=target_language,
            model=model,
        )
        for item in items
    ]


def main() -> None:
    import json
    import sys

    if len(sys.argv) < 4:
        raise SystemExit("usage: quality_summary.py <source_text> <translated_text> <target_language>")
    result = summarize_translation_quality(sys.argv[1], sys.argv[2], sys.argv[3])
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
