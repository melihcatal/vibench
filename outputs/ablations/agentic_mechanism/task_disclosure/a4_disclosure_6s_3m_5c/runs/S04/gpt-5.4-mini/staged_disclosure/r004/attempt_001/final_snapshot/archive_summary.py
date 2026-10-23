import os
from typing import Any, Dict, List

from openai import OpenAI


def _extract_text(result: Any) -> str:
    if isinstance(result, str):
        return result
    if isinstance(result, dict):
        for key in ("summary", "text", "content", "transcript", "output"):
            value = result.get(key)
            if isinstance(value, str) and value.strip():
                return value
        parts: List[str] = []
        for key in ("segments", "items", "chunks", "results"):
            value = result.get(key)
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, dict):
                        text = item.get("text") or item.get("content") or item.get("transcript")
                        if isinstance(text, str) and text.strip():
                            parts.append(text.strip())
                    elif isinstance(item, str) and item.strip():
                        parts.append(item.strip())
        if parts:
            return "\n".join(parts)
    return str(result)


def summarize_transcription_results(transcription_results: Any) -> str:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    transcript_text = _extract_text(transcription_results)
    response = client.responses.create(
        model="gpt-5.4-mini",
        input=[
            {
                "role": "system",
                "content": "Summarize transcription results concisely, preserving key points, decisions, action items, and names.",
            },
            {"role": "user", "content": transcript_text},
        ],
    )
    summary = getattr(response, "output_text", None)
    if isinstance(summary, str) and summary.strip():
        return summary.strip()
    output = getattr(response, "output", None)
    if isinstance(output, list):
        collected: List[str] = []
        for item in output:
            content = getattr(item, "content", None)
            if isinstance(content, list):
                for part in content:
                    text = getattr(part, "text", None)
                    if isinstance(text, str) and text.strip():
                        collected.append(text.strip())
        if collected:
            return "\n".join(collected)
    return ""


def main() -> None:
    import json
    import sys

    if len(sys.argv) > 1:
        payload = json.loads(sys.argv[1])
    else:
        payload = json.loads(sys.stdin.read() or "{}")
    print(summarize_transcription_results(payload))


if __name__ == "__main__":
    main()
