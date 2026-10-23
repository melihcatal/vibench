import json
import os
from typing import Any, Dict, Optional

from openai import OpenAI


MODEL_ID = "gpt-5.4-mini"


def _read_text_from_asset(asset_path: str) -> str:
    with open(asset_path, "r", encoding="utf-8") as handle:
        return handle.read()


def summarize_stored_asset(asset_path: str, instruction: Optional[str] = None) -> str:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    content = _read_text_from_asset(asset_path)
    prompt = instruction or "Summarize the content extracted from this stored asset concisely and accurately."
    response = client.responses.create(
        model=MODEL_ID,
        input=[
            {
                "role": "system",
                "content": "You summarize extracted asset content clearly and faithfully.",
            },
            {
                "role": "user",
                "content": f"{prompt}\n\nAsset content:\n{content}",
            },
        ],
    )
    return response.output_text


def main() -> None:
    asset_path = os.environ.get("STORED_ASSET_PATH", "stored_asset.txt")
    instruction = os.environ.get("SUMMARY_INSTRUCTION")
    summary = summarize_stored_asset(asset_path, instruction)
    print(summary)


if __name__ == "__main__":
    main()
