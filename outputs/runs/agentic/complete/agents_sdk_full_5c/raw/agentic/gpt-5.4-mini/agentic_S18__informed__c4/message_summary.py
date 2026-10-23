from __future__ import annotations

from openai import OpenAI

from messaging_models import MessageSummary

MODEL_ID = "gpt-4o-mini"


def message_summary(total: int, succeeded: int, failed: int, provider: str = "OpenAI") -> MessageSummary:
    client = OpenAI()
    prompt = f"Summarize pub/sub processing results: total={total}, succeeded={succeeded}, failed={failed}."
    response = client.chat.completions.create(model=MODEL_ID, messages=[{"role": "user", "content": prompt}])
    summary = response.choices[0].message.content or ""
    return MessageSummary(total=total, succeeded=succeeded, failed=failed, provider=provider, summary=summary)
