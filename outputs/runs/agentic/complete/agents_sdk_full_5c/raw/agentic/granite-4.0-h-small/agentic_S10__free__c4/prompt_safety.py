import os
from model_client import get_llm_client
from model_models import LLMResponse

def is_prompt_safe(user_prompt: str, model_name: str = "gpt-4o-mini") -> bool:
    """Check whether a user prompt may contain disallowed or unsafe content.
    Uses a hosted LLM moderation endpoint (OpenAI moderation API) for detection.
    Identifies provider via SDK import and model identifier.
    Returns True if safe, False otherwise.
    """
    client = get_llm_client(model_name)
    # OpenAI moderation endpoint expects a list of texts
    response = client.moderations.create(
        input=user_prompt,
    )
    result = response.results[0]
    flagged_categories = {
        "hate", "hate/threatening", "self-harm", "sexual", "sexual/minors",
        "violence", "violence/graphic"
    }
    for category, flagged in result.flagged_categories.items():
        if flagged and category in flagged_categories:
            return False
    return True
