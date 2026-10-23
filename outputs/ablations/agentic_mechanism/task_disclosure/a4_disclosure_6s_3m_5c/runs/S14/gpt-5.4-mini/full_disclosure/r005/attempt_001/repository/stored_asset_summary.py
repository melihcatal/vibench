import os
from typing import Any, Dict, List, Optional

import openai


def _get_client() -> openai.OpenAI:
    return openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def summarize_stored_asset(
    extracted_text: str,
    *,
    asset_name: Optional[str] = None,
    max_bullets: int = 5,
) -> Dict[str, Any]:
    client = _get_client()
    prompt_parts: List[str] = [
        "Summarize the extracted content from a stored asset.",
        f"Limit the summary to {max_bullets} concise bullets.",
        "Include the key topics, facts, and any notable entities.",
    ]
    if asset_name:
        prompt_parts.append(f"Asset name: {asset_name}")
    prompt_parts.append("Extracted text:\n" + extracted_text)

    response = client.responses.create(
        model="gpt-5.4-mini",
        input=[
            {
                "role": "system",
                "content": "You are a concise document summarizer for stored assets.",
            },
            {"role": "user", "content": "\n\n".join(prompt_parts)},
        ],
    )

    summary_text = getattr(response, "output_text", None)
    if not summary_text:
        summary_text = ""

    return {
        "asset_name": asset_name,
        "summary": summary_text,
        "model": "gpt-5.4-mini",
    }


def main() -> None:
    extracted_text = os.getenv("STORED_ASSET_TEXT", "")
    asset_name = os.getenv("STORED_ASSET_NAME")
    result = summarize_stored_asset(extracted_text, asset_name=asset_name)
    print(result["summary"])


if __name__ == "__main__":
    main()
