import os
import requests
from typing import List, Dict, Any, Optional

from speech_models import TranscriptSummary

OPENAI_CHAT_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_SUMMARY_MODEL = "gpt-4o-mini"


def get_openai_api_key() -> str:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is not set")
    return api_key


def generate_summary(
    transcript_text: str,
    include_key_points: bool = True,
    include_action_items: bool = True,
    include_sentiment: bool = True,
) -> Dict[str, Any]:
    api_key = get_openai_api_key()

    prompt_parts = [
        "You are an expert meeting summarizer. Analyze the following transcript and provide:",
        "1. A concise title for the meeting",
        "2. A brief summary paragraph",
    ]
    if include_key_points:
        prompt_parts.append("3. Key discussion points as a bulleted list")
    if include_action_items:
        prompt_parts.append("4. Action items with responsible parties if mentioned")
    if include_sentiment:
        prompt_parts.append("5. Overall sentiment (positive, neutral, or negative)")

    prompt_parts.append(f"\nTranscript:\n{transcript_text}")

    system_prompt = (
        "Respond in valid JSON format with keys: title, summary, key_points (list), "
        "action_items (list), sentiment. Return empty lists if not applicable."
    )

    response = requests.post(
        OPENAI_CHAT_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": OPENAI_SUMMARY_MODEL,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": "\n".join(prompt_parts)},
            ],
            "temperature": 0.3,
            "max_tokens": 1000,
        },
    )
    response.raise_for_status()
    data = response.json()

    import json

    content = data["choices"][0]["message"]["content"].strip()
    try:
        summary_data = json.loads(content)
    except json.JSONDecodeError:
        summary_data = {
            "title": "Meeting Summary",
            "summary": content,
            "key_points": [],
            "action_items": [],
            "sentiment": "unknown",
        }

    word_count = len(transcript_text.split())
    speaker_count = transcript_text.count("]:") if "]:" in transcript_text else 1

    return {
        "provider": "OpenAI",
        "model": OPENAI_SUMMARY_MODEL,
        "title": summary_data.get("title", ""),
        "summary": summary_data.get("summary", ""),
        "key_points": summary_data.get("key_points", []),
        "action_items": summary_data.get("action_items", []),
        "sentiment": summary_data.get("sentiment"),
        "word_count": word_count,
        "speaker_count": speaker_count,
        "usage": {
            "prompt_tokens": data.get("usage", {}).get("prompt_tokens", 0),
            "completion_tokens": data.get("usage", {}).get("completion_tokens", 0),
        },
    }


def archive_summary(transcript_data: Dict[str, Any], **kwargs) -> Dict[str, Any]:
    text = transcript_data.get("text", "")
    if not text:
        utterances = transcript_data.get("utterances", [])
        text = " ".join(u.get("text", "") for u in utterances)

    return generate_summary(text, **kwargs)


if __name__ == "__main__":
    import sys

    text = sys.argv[1] if len(sys.argv) > 1 else ""
    if not text:
        print("Usage: python archive_summary.py <transcript_text>")
        sys.exit(1)

    result = generate_summary(text)
    print(result)
