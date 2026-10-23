import os
from typing import Any, Dict, List, Optional

from openai import OpenAI


def _get_client() -> OpenAI:
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def summarize_message_processing_results(messages: List[Dict[str, Any]], model: str = "gpt-5.4-mini") -> str:
    client = _get_client()
    payload = {
        "messages": messages,
        "task": "Summarize message processing results in a concise, structured way.",
    }
    response = client.responses.create(
        model=model,
        input=[
            {
                "role": "system",
                "content": "You summarize message processing results succinctly and accurately.",
            },
            {
                "role": "user",
                "content": str(payload),
            },
        ],
    )
    return response.output_text


def summarize_results(messages: List[Dict[str, Any]]) -> str:
    return summarize_message_processing_results(messages)


def main() -> None:
    raise SystemExit("This module provides summarize_message_processing_results and summarize_results.")


if __name__ == "__main__":
    main()
