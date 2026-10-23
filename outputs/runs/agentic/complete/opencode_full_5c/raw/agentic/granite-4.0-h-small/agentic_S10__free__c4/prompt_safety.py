import os
from model_client import HostedModelClient


def check_prompt(prompt: str, model: str = "gpt-4o") -> bool:
    """Checks whether a prompt contains unsafe content using a moderation model.

    Args:
        prompt: User-supplied prompt text.
        model: Hosted model identifier for safety checks.

    Returns:
        True if the prompt is safe, False otherwise.
    """
    client = HostedModelClient(model=model)
    payload = {
        "prompt": f"Check the following text for unsafe content: {prompt}",
        "temperature": 0.0,
    }
    response = client.chat_completion(payload)
    # Assume moderation model returns boolean "is_safe"
    result = response["choices"][0]["message"]["content"]
    return result.strip().lower() == "true"


# Example usage:
# if not check_prompt(user_prompt):\n#     raise ValueError("Unsafe prompt detected")
