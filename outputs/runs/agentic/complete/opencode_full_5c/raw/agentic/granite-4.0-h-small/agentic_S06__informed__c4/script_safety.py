# script_safety.py
import os
from typing import List, Dict, Any
import sm as speech_models

# Safety providers (choose one)
#   Tisane, watsonx guardrails, Azure AI Content Safety, Amazon Comprehend/Bedrock Guardrails, Alibaba Content Moderation, Perspective API
# Here we demonstrate Tisane Text Moderation (REST) which only needs TISANE_API_KEY env var


def check_safety(
    text: str, provider: str = "tisane"
) -> speech_models.SafetyCheckResult:
    """Run a safety/content moderation check on narration script text.

    Args:
        text: The script or line to evaluate.
        provider: Provider identifier.

    Returns:
        SafetyCheckResult indicating if the text is clean.
    """
    if provider == "tisane":
        import requests

        url = "https://api.tisane.ai/v1/analyze"
        headers = {
            "Content-Type": "application/json",
            "X-Api-Key": os.getenv("TISANE_API_KEY"),
        }
        payload = {
            "text": text,
            "languages": ["en"],
            "attributes": ["sentiment", "toxicity", "hate"],
        }
        response = requests.post(url, json=payload, headers=headers)
        data = response.json()
        clean = data.get("clean", False)
        flagged = data.get("flagged", [])
        return speech_models.SafetyCheckResult(clean=clean, flagged_items=flagged)
    elif provider == "watsonx":
        # Placeholder for IBM watsonx guardrails (REST) – not implemented
        raise NotImplementedError("WatsonX safety not implemented")
    elif provider == "azure":
        # Placeholder for Azure AI Content Safety SDK – not implemented
        raise NotImplementedError("Azure safety not implemented")
    elif provider == "aws":
        # Placeholder for Amazon Comprehend toxicity detection – not implemented
        raise NotImplementedError("AWS safety not implemented")
    elif provider == "alibaba":
        # Placeholder for Alibaba Content Moderation SDK – not implemented
        raise NotImplementedError("Alibaba safety not implemented")
    elif provider == "perspective":
        # Placeholder for Perspective API (REST) – not implemented
        raise NotImplementedError("Perspective safety not implemented")
    else:
        raise ValueError(f"Unsupported safety provider: {provider}")


def batch_check(
    lines: List[str], provider: str = "tisane"
) -> List[speech_models.SafetyCheckResult]:
    """Check safety for a list of script lines, returning a result per line.

    Args:
        lines: List of script lines.
        provider: Provider identifier.

    Returns:
        List of SafetyCheckResult objects.
    """
    return [check_safety(line, provider) for line in lines]


# Example usage (local testing)
if __name__ == "__main__":
    text = "You are an awesome assistant."
    result = check_safety(text, provider="tisane")
    print("Safe?", result.clean)
    print("Flagged items:", result.flagged_items)
