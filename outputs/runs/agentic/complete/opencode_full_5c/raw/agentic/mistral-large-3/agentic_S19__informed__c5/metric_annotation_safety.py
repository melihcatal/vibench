from anthropic import Anthropic
import os
from typing import List, Dict, Optional
from .observability_client import get_client


def check_unsafe_text(
    text: str,
    threshold: float = 0.7,
) -> Dict[str, Union[bool, float, str]]:
    """
    Checks free-text metric labels or annotations for unsafe text using Anthropic's moderation API.

    Args:
        text: The text to check for unsafe content.
        threshold: The confidence threshold for flagging unsafe content.

    Returns:
        Dict: A dictionary containing the safety check results.
    """
    client = get_client("anthropic", Anthropic)

    prompt = (
        f"Analyze the following text for unsafe content, including hate speech, harassment, violence, "
        f"self-harm, sexual content, or dangerous content. Provide a confidence score between 0 and 1 "
        f"indicating the likelihood of unsafe content.\n\n"
        f"Text: {text}\n\n"
        f"Respond in JSON format with the following keys: 'is_unsafe', 'confidence', 'reason'."
    )

    response = client.messages.create(
        model="claude-3-sonnet-20240229",
        max_tokens=150,
        messages=[{"role": "user", "content": prompt}],
    )

    result = response.content[0].text.strip()
    try:
        import json

        result_dict = json.loads(result)
        result_dict["confidence"] = float(result_dict["confidence"])
        result_dict["is_unsafe"] = result_dict["confidence"] >= threshold
        return result_dict
    except Exception as e:
        return {
            "is_unsafe": False,
            "confidence": 0.0,
            "reason": f"Failed to parse response: {str(e)}",
        }
