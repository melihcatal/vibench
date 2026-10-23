from __future__ import annotations

from datetime import datetime, timezone

from openai import OpenAI

from messaging_models import normalize_text


MODEL = "gpt-4o-mini"


def summarize_messages(messages: list[dict]) -> dict:
    client = OpenAI()
    joined = "\n".join(f"- {normalize_text(msg.get('text') or msg.get('payload') or msg)}" for msg in messages)
    prompt = f"Summarize these message processing results in concise bullet points:\n{joined}"
    completion = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You summarize operational message processing results."},
            {"role": "user", "content": prompt},
        ],
    )
    return {
        "provider": "openai",
        "model": MODEL,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "summary": completion.choices[0].message.content,
    }
