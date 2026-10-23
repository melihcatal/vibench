from model_client import get_moderation_model, get_openai_client
from model_models import SafetyResult, normalize_categories


def check_prompt_safety(prompt: str, generated_text: str = "") -> SafetyResult:
    client = get_openai_client()
    response = client.moderations.create(
        model=get_moderation_model(),
        input=[prompt, generated_text],
    )
    result = response.results[0]
    return SafetyResult(
        provider="OpenAI",
        model=get_moderation_model(),
        flagged=bool(result.flagged),
        categories=normalize_categories(result.categories),
    )
