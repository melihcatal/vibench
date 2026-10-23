import os
import requests
from typing import Dict, Any, List


def check_prompt_safety(prompt: str, generated_text: str = "") -> Dict[str, Any]:
    """
    Check prompts and generated text for unsafe content using Tisane API.
    """
    api_key = os.getenv("TISANE_API_KEY")
    if not api_key:
        raise ValueError("TISANE_API_KEY environment variable is required")

    url = "https://api.tisane.ai/v1/content/moderation"

    headers = {"Content-Type": "application/json", "X-API-Key": api_key}

    payload = {"content": prompt, "language": "en", "include_feedback": True}

    if generated_text:
        payload["content"] = f"{prompt}\n\nGenerated: {generated_text}"

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()

    result = response.json()

    # Extract safety information
    is_safe = True
    issues = []

    if "abuse" in result:
        abuse_data = result["abuse"]
        if abuse_data.get("has_abuse", False):
            is_safe = False
            issues.append("Contains abusive content")

    if "hate_speech" in result:
        hate_data = result["hate_speech"]
        if hate_data.get("has_hate_speech", False):
            is_safe = False
            issues.append("Contains hate speech")

    if "sexual_content" in result:
        sexual_data = result["sexual_content"]
        if sexual_data.get("has_sexual_content", False):
            is_safe = False
            issues.append("Contains sexual content")

    return {
        "is_safe": is_safe,
        "issues": issues,
        "raw_result": result,
        "score": result.get("overall_risk_score", 0.0),
    }
