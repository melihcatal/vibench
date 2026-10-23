import os
from model_client import get_llm_client
from model_models import InferenceResponse

def is_prompt_safe(text: str, model_family: str = "gpt-4") -> bool:
    """Check a user prompt for unsafe content using a hosted moderation model.

    Args:
        text: The raw prompt to evaluate.
        model_family: LLM family/model identifier for moderation (default: "gpt-4").

    Returns:
        True if the prompt passes moderation, False otherwise.
    """
    client = get_llm_client(model_family)
    payload = {
        "model": model_family,
        "prompt": f"You are a content safety moderator. Return {'PASS' if is_safe(text) else 'BLOCK'} after analyzing:\n\n{text}"
    }
    # NOTE: The above is illustrative. In practice you would call a dedicated moderation endpoint
    # or a separate model like 'moderation-001'. For demo purposes we simulate:
    response = client.chat_completion(payload)  # type: ignore
    decision = response.choices[0].message.content.strip().upper()
    return decision == "PASS"

def is_safe(text: str) -> bool:
    """Placeholder for real safety check logic.

    Replace with actual provider moderation API call.
    """
    # Simulated safe output
    return True
