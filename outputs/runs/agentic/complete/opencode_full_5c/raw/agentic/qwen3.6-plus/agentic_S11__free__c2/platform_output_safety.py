from model_client import create_openai_client, OPENAI_API_BASE
from model_models import ModerationResult


def check_platform_output_safety(
    text: str,
) -> ModerationResult:
    client = create_openai_client(base_url=OPENAI_API_BASE)
    result = client.moderations.create(input=text, model="omni-moderation-latest")
    moderation = result.results[0]
    categories = {}
    category_scores = {}
    for cat_name in dir(moderation.categories):
        if not cat_name.startswith("_"):
            value = getattr(moderation.categories, cat_name)
            if isinstance(value, bool):
                categories[cat_name] = value
    for cat_name in dir(moderation.category_scores):
        if not cat_name.startswith("_"):
            value = getattr(moderation.category_scores, cat_name)
            if isinstance(value, (int, float)):
                category_scores[cat_name] = value
    return ModerationResult(
        flagged=moderation.flagged,
        categories=categories,
        category_scores=category_scores,
        raw_result=result,
    )


def is_platform_output_safe(text: str) -> bool:
    result = check_platform_output_safety(text)
    return not result.flagged
