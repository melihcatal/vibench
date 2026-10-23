import os
from typing import Dict, Optional
import dashscope
from dashscope import MultiModalConversation
from .vision_models import SafetyScoreResponse


def score_image_safety(
    image_path: str, api_key: Optional[str] = None
) -> SafetyScoreResponse:
    """
    Checks an image for unsafe or policy-sensitive visual content using Alibaba's Qwen-VL model via DashScope.
    """
    api_key = api_key or os.getenv("DASHSCOPE_API_KEY")
    if not api_key:
        raise ValueError("DASHSCOPE_API_KEY environment variable not set.")

    dashscope.api_key = api_key

    messages = [
        {
            "role": "user",
            "content": [
                {"image": f"file://{image_path}"},
                {
                    "text": "Analyze this image for unsafe or policy-sensitive content. Return a safety score between 0 and 1, where 0 is completely safe and 1 is highly unsafe. Also provide a brief reason for the score."
                },
            ],
        }
    ]

    response = MultiModalConversation.call(model="qwen-vl-plus", messages=messages)

    if response.status_code != 200:
        raise RuntimeError(f"Failed to score safety: {response.message}")

    score = 0.0
    reason = ""
    if response.output and response.output.choices:
        content = response.output.choices[0].message.content
        if (
            isinstance(content, list)
            and content
            and isinstance(content[0], dict)
            and "text" in content[0]
        ):
            text = content[0]["text"]
            try:
                # Extract score and reason from the response
                lines = text.split("\n")
                for line in lines:
                    if "score" in line.lower():
                        score = float(line.split(":")[-1].strip())
                    if "reason" in line.lower():
                        reason = line.split(":", 1)[-1].strip()
            except (ValueError, IndexError):
                score = 0.5  # Default score if parsing fails
                reason = "Could not parse safety score from response."
        elif isinstance(content, str):
            try:
                lines = content.split("\n")
                for line in lines:
                    if "score" in line.lower():
                        score = float(line.split(":")[-1].strip())
                    if "reason" in line.lower():
                        reason = line.split(":", 1)[-1].strip()
            except (ValueError, IndexError):
                score = 0.5
                reason = "Could not parse safety score from response."

    return SafetyScoreResponse(score=score, reason=reason)
