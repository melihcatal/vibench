"""
image_summary.py - Summarize visual analysis results
using Mistral Chat API for hosted LLM inference.
"""

import json
import os
import sys
from typing import Dict, Any, Optional

import mistralai
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage

from vision_models import VisionAnalysisResponse


MISTRAL_MODEL = "mistral-large-latest"
MISTRAL_API_KEY_ENV = "MISTRAL_API_KEY"


def get_mistral_api_key() -> str:
    key = os.environ.get(MISTRAL_API_KEY_ENV)
    if not key:
        raise RuntimeError(f"Missing environment variable: {MISTRAL_API_KEY_ENV}")
    return key


def create_mistral_client() -> MistralClient:
    """Create a Mistral client using MISTRAL_API_KEY."""
    api_key = get_mistral_api_key()
    return MistralClient(api_key=api_key)


def summarize_visual_analysis(
    analysis_data: Dict[str, Any],
    *,
    client: Optional[MistralClient] = None,
    model: str = MISTRAL_MODEL,
) -> str:
    """
    Summarize visual analysis results using Mistral Chat API.

    Provider: Mistral Chat API (mistralai)
    Auth: MISTRAL_API_KEY
    Model: mistral-large-latest
    """
    if client is None:
        client = create_mistral_client()

    payload_json = json.dumps(analysis_data, indent=2, ensure_ascii=False)

    system_prompt = (
        "You are an assistant that summarizes visual image analysis results. "
        "Provide a concise, clear summary of the detected labels, descriptions, "
        "extracted text, and any safety concerns. Keep the summary under 150 words."
    )

    messages = [
        ChatMessage(role="system", content=system_prompt),
        ChatMessage(
            role="user",
            content=(
                f"Here are the visual analysis results for an image:\n\n"
                f"{payload_json}\n\n"
                f"Please provide a concise summary."
            ),
        ),
    ]

    response = client.chat(
        model=model,
        messages=messages,
        max_tokens=500,
        temperature=0.3,
    )

    summary = response.choices[0].message.content if response.choices else ""
    return summary.strip()


def summarize_from_file(
    input_file: str,
    *,
    client: Optional[MistralClient] = None,
) -> str:
    """Load analysis data from a JSON file and produce a summary."""
    with open(input_file, "r", encoding="utf-8") as f:
        analysis_data = json.load(f)
    return summarize_visual_analysis(analysis_data, client=client)


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python image_summary.py <analysis_json_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    summary = summarize_from_file(input_file)
    print("=== Visual Analysis Summary ===")
    print(summary)


if __name__ == "__main__":
    main()
