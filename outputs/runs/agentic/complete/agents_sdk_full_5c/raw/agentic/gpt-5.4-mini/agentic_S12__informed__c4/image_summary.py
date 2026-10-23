import os
from typing import Iterable

from anthropic import Anthropic

from vision_models import ImageAnalysisResult


MODEL_ID = os.environ.get("ANTHROPIC_MODEL", "claude-3-5-sonnet-20240620")


def summarize_visual_analysis(result: ImageAnalysisResult) -> str:
    client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
    prompt = f"Summarize this image analysis in one short sentence:\n{result.to_dict()}"
    message = client.messages.create(
        model=MODEL_ID,
        max_tokens=80,
        messages=[{"role": "user", "content": prompt}],
    )
    return "".join(block.text for block in message.content if hasattr(block, "text"))
