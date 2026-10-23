from __future__ import annotations

import argparse

from storage_client import get_bedrock_runtime_client, load_settings
from storage_models import SummaryResult


MODEL_ID = "anthropic.claude-3-haiku-20240307-v1:0"


def summarize_stored_asset(source_text: str) -> SummaryResult:
    bedrock = get_bedrock_runtime_client()
    prompt = f"Summarize the following asset content in 3-5 concise bullets:\n\n{source_text}"
    response = bedrock.converse(
        modelId=MODEL_ID,
        messages=[{"role": "user", "content": [{"text": prompt}]}],
        inferenceConfig={"maxTokens": 300, "temperature": 0.2},
    )
    summary = ""
    for item in response.get("output", {}).get("message", {}).get("content", []):
        if "text" in item:
            summary += item["text"]
    return SummaryResult(source_text=source_text, summary=summary)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("text")
    args = parser.parse_args()
    _ = load_settings()
    print(summarize_stored_asset(args.text))
