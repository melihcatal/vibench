import json
import os
from typing import Any, Dict, List, Optional

import requests


OPENAI_RESPONSES_API_URL = "https://api.openai.com/v1/responses"
OPENAI_MODEL = "gpt-4.1-mini"


def _extract_text(item: Any) -> str:
    if item is None:
        return ""
    if isinstance(item, str):
        return item
    if isinstance(item, dict):
        for key in ("text", "content", "summary", "snippet", "title"):
            value = item.get(key)
            if isinstance(value, str) and value.strip():
                return value.strip()
        return json.dumps(item, ensure_ascii=False)
    return str(item)


def _normalize_results(retrieved_results: Any) -> List[str]:
    if retrieved_results is None:
        return []
    if isinstance(retrieved_results, str):
        return [retrieved_results]
    if isinstance(retrieved_results, dict):
        for key in ("results", "items", "documents", "hits", "records"):
            value = retrieved_results.get(key)
            if isinstance(value, list):
                return [_extract_text(v) for v in value if _extract_text(v)]
        return [_extract_text(retrieved_results)]
    if isinstance(retrieved_results, list):
        return [_extract_text(v) for v in retrieved_results if _extract_text(v)]
    return [_extract_text(retrieved_results)]


def generate_retrieval_audio_brief(
    retrieved_results: Any,
    topic: Optional[str] = None,
    audience: Optional[str] = None,
    api_key: Optional[str] = None,
    model: str = OPENAI_MODEL,
) -> str:
    texts = _normalize_results(retrieved_results)
    if not texts:
        return "No relevant results were found."

    prompt_parts = []
    if topic:
        prompt_parts.append(f"Topic: {topic}")
    if audience:
        prompt_parts.append(f"Audience: {audience}")
    prompt_parts.append("Retrieved results:")
    prompt_parts.extend(f"- {text}" for text in texts[:10])
    prompt_parts.append(
        "Write a short spoken brief that sounds natural when read aloud, summarizes the key points, and avoids bullets or markdown."
    )
    prompt = "\n".join(prompt_parts)

    key = api_key or os.getenv("OPENAI_API_KEY")
    if not key:
        raise ValueError("OPENAI_API_KEY is required")

    payload: Dict[str, Any] = {
        "model": model,
        "input": prompt,
    }
    response = requests.post(
        OPENAI_RESPONSES_API_URL,
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()

    if isinstance(data, dict):
        for key_name in ("output_text", "text"):
            value = data.get(key_name)
            if isinstance(value, str) and value.strip():
                return value.strip()
        output = data.get("output")
        if isinstance(output, list):
            chunks: List[str] = []
            for item in output:
                if not isinstance(item, dict):
                    continue
                contents = item.get("content")
                if isinstance(contents, list):
                    for content in contents:
                        if isinstance(content, dict):
                            text = content.get("text")
                            if isinstance(text, str) and text.strip():
                                chunks.append(text.strip())
            if chunks:
                return "\n".join(chunks).strip()

    return json.dumps(data, ensure_ascii=False)
