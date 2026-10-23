import os
from openai import OpenAI
from openai.types import ModerationCreateResponse
from observability_models import TextSafetyResult


OPENAI_MODERATION_MODEL = "omni-moderation-2024-09-26"


def check_log_text_safety(text: str) -> TextSafetyResult:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")

    client = OpenAI(api_key=api_key)

    response: ModerationCreateResponse = client.moderations.create(
        model=OPENAI_MODERATION_MODEL,
        input=text,
    )

    result = response.results[0]
    flagged = result.flagged
    categories = {}
    flags = []

    for category, is_flagged in result.categories.model_dump().items():
        categories[category] = result.category_scores.model_dump().get(category, 0.0)
        if is_flagged:
            flags.append(category)

    return TextSafetyResult(
        text=text,
        is_safe=not flagged,
        flags=flags,
        categories={k: round(v, 4) for k, v in categories.items()},
        model_used=OPENAI_MODERATION_MODEL,
    )


def check_multiple_log_texts(texts: list[str]) -> list[TextSafetyResult]:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")

    client = OpenAI(api_key=api_key)

    response: ModerationCreateResponse = client.moderations.create(
        model=OPENAI_MODERATION_MODEL,
        input=texts,
    )

    results = []
    for text, mod_result in zip(texts, response.results):
        flagged = mod_result.flagged
        categories = {}
        flags = []

        for category, is_flagged in mod_result.categories.model_dump().items():
            categories[category] = mod_result.category_scores.model_dump().get(
                category, 0.0
            )
            if is_flagged:
                flags.append(category)

        results.append(
            TextSafetyResult(
                text=text,
                is_safe=not flagged,
                flags=flags,
                categories={k: round(v, 4) for k, v in categories.items()},
                model_used=OPENAI_MODERATION_MODEL,
            )
        )

    return results


if __name__ == "__main__":
    sample_log = "User login failed: invalid credentials for admin@example.com from IP 192.168.1.100"
    result = check_log_text_safety(sample_log)
    print(result.model_dump_json(indent=2))
