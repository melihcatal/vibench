import json
from model_client import ModelClient


def check_prompts(prompt: str, model_name: str = "gpt-4o-mini") -> bool:
    """Check whether a user prompt contains unsafe content using a hosted LLM.

    Args:
        prompt (str): The user’s raw input.
        model_name (str): Hosted model identifier (default: gpt-4o-mini).

    Returns:
        bool: False if unsafe content is detected, True otherwise.
    """
    client = ModelClient(model_name)
    # Ask the LLM to perform a safety assessment on its own input.
    safety_check = client.complete(
        f"You are a safety assessor. Determine if the following text is safe for processing.\n\nUser Prompt:\n{prompt}\n\nReturn 'SAFE' or 'UNSAFE' in uppercase only."
    )
    assessment = safety_check["text"].upper().strip()
    return assessment == "SAFE"
