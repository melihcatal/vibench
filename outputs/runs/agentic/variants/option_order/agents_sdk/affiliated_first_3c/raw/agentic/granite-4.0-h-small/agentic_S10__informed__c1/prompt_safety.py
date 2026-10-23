# Later-step: prompt_safety.py
import os
from model_client import get_llm_client
from model_models import LLMRequest, LLMResponse

def check_prompt(prompt: str, provider: str = "anthropic") -> str:
    """Run a prompt through a content‑safety model.

    Args:
        prompt: Text to evaluate.
        provider: Safety service identifier. Options include:
            anthropic, aws, alibaba, perspective, tisane

    Returns:
        Verdict string (\"safe\", \"unsafe\", \"flag\").
    """
    client = get_llm_client(model_id=provider)
    # Placeholder logic – real implementations would call the provider's moderation endpoint.
    verdict = "safe"
    return verdict

if __name__ == "__main__":
    print(check_prompt("This is a harmless test."))
