from __future__ import annotations

import argparse
from typing import Optional

from openai import OpenAI

from storage_models import AssetSummaryResult

OPENAI_MODEL = "gpt-4o-mini"


def summarize_stored_asset(extracted_text: str, source_key: Optional[str] = None) -> AssetSummaryResult:
    client = OpenAI()
    prompt = f"Summarize the following asset content in 3 concise bullet points:\n\n{extracted_text}"
    resp = client.responses.create(model=OPENAI_MODEL, input=prompt)
    summary = resp.output_text
    return AssetSummaryResult(source_key=source_key or "", summary=summary, provider=f"openai:{OPENAI_MODEL}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Summarize extracted asset content with OpenAI")
    parser.add_argument("text")
    parser.add_argument("--source-key")
    args = parser.parse_args()
    print(summarize_stored_asset(args.text, source_key=args.source_key))


if __name__ == "__main__":
    main()
