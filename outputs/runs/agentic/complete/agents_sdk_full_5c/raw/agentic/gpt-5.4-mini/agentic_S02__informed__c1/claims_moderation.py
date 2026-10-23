from __future__ import annotations

from typing import Iterable

from anthropic import Anthropic


MODEL_ID = "claude-3-5-sonnet-20240620"


def moderate_claim_text(text: str, categories: Iterable[str] = ()) -> str:
    client = Anthropic()
    prompt = f"Review this federated identity claim text for toxicity or policy issues. Categories: {', '.join(categories)}\n\n{text}"
    msg = client.messages.create(
        model=MODEL_ID,
        max_tokens=200,
        messages=[{"role": "user", "content": prompt}],
    )
    return msg.content[0].text if msg.content else ""
