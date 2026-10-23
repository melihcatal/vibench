import json
import os
from typing import Any, Dict, List, Optional

from openai import OpenAI


def _extract_text(transcription_result: Any) -> str:
    if isinstance(transcription_result, str):
        return transcription_result.strip()
    if isinstance(transcription_result, dict):
        for key in ("text", "transcript", "content", "summary"):
            value = transcription_result.get(key)
            if isinstance(value, str) and value.strip():
                return value.strip()
        return json.dumps(transcription_result, ensure_ascii=False)
    return str(transcription_result).strip()


def _chunk_text(text: str, max_chars: int = 12000) -> List[str]:
    text = text.strip()
    if not text:
        return []
    if len(text) <= max_chars:
        return [text]
    chunks = []
    start = 0
    while start < len(text):
        end = min(len(text), start + max_chars)
        if end < len(text):
            split_at = text.rfind("\n", start, end)
            if split_at <= start:
                split_at = text.rfind(". ", start, end)
                if split_at > start:
                    end = split_at + 1
                else:
                    end = max(start + 1, end)
            else:
                end = split_at
        chunks.append(text[start:end].strip())
        start = end
    return [chunk for chunk in chunks if chunk]


def _openai_client() -> OpenAI:
    api_key = os.getenv("OPENAI_API_KEY")
    return OpenAI(api_key=api_key) if api_key else OpenAI()


def summarize_transcription_results(transcription_result: Any, model: str = "gpt-4o-mini") -> str:
    text = _extract_text(transcription_result)
    if not text:
        return ""

    client = _openai_client()
    chunks = _chunk_text(text)

    if len(chunks) == 1:
        response = client.responses.create(
            model=model,
            input=[
                {
                    "role": "system",
                    "content": "You summarize transcription results into a concise archive-ready summary.",
                },
                {
                    "role": "user",
                    "content": f"Summarize the following transcription results in 3-6 bullet points, capturing key topics, decisions, action items, and notable entities:\n\n{text}",
                },
            ],
        )
        return response.output_text.strip()

    intermediate_summaries = []
    for idx, chunk in enumerate(chunks, start=1):
        response = client.responses.create(
            model=model,
            input=[
                {
                    "role": "system",
                    "content": "You summarize parts of a larger transcript for later consolidation.",
                },
                {
                    "role": "user",
                    "content": f"Part {idx} of {len(chunks)}:\n\n{chunk}\n\nProduce a compact bullet summary of this part.",
                },
            ],
        )
        intermediate_summaries.append(response.output_text.strip())

    combined = "\n\n".join(intermediate_summaries)
    final_response = client.responses.create(
        model=model,
        input=[
            {
                "role": "system",
                "content": "You consolidate multiple transcript summaries into one archive-ready summary.",
            },
            {
                "role": "user",
                "content": f"Consolidate these partial summaries into 3-6 concise bullet points:\n\n{combined}",
            },
        ],
    )
    return final_response.output_text.strip()


def summarize_from_file(path: str, model: str = "gpt-4o-mini") -> str:
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    return summarize_transcription_results(content, model=model)
