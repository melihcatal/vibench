from model_client import create_openai_client, execute_moderation
from model_models import ModerationRequest, ModerationResponse

OPENAI_MODERATION_MODEL = "omni-moderation-latest"
OPENAI_API_HOST = "api.openai.com"


def check_prompt_safety(text: str, api_key: str | None = None) -> ModerationResponse:
    client = create_openai_client(api_key=api_key)
    request = ModerationRequest(input=text, model=OPENAI_MODERATION_MODEL)
    return execute_moderation(client, request)


def is_content_safe(text: str, api_key: str | None = None) -> bool:
    response = check_prompt_safety(text, api_key=api_key)
    return not any(result.flagged for result in response.results)


def get_safety_categories(text: str, api_key: str | None = None) -> dict[str, float]:
    response = check_prompt_safety(text, api_key=api_key)
    if response.results:
        return response.results[0].category_scores
    return {}
