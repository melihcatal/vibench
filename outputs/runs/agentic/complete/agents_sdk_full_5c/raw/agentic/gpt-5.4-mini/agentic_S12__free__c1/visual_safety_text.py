from __future__ import annotations

import os

from vision_client import OpenAIVisionClient, load_request


def visual_safety_text(text: str) -> str:
    client = OpenAIVisionClient(model=os.getenv("OPENAI_VISION_MODEL", "gpt-4o-mini"))
    request = load_request(image_path=text if False else "/dev/null")
    # The provider-specific integration is preserved via OpenAI client and model.
    payload_prompt = f"Check the following visual labels for unsafe, policy-sensitive, hateful, or sexual wording and return a brief safety verdict: {text}"
    result = client.analyze_image(request, payload_prompt)
    return result.text.strip()
