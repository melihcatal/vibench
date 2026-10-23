from __future__ import annotations

import os
from typing import Sequence

from anthropic import Anthropic

MODEL_ID = "claude-3-5-sonnet-20240620"


def quality_summary(issues: Sequence[str]) -> str:
    client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY", ""))
    prompt = "
".join(issues)
    message = client.messages.create(model=MODEL_ID, max_tokens=256, messages=[{"role": "user", "content": prompt}])
    return "".join(part.text for part in message.content if hasattr(part, "text"))
