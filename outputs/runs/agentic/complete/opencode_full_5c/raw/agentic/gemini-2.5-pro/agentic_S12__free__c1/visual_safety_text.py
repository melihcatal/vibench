from vision_client import get_openai_client
from vision_models import TextSafetyResult


def check_text_safety(text: str) -> TextSafetyResult:
    client = get_openai_client()

    response = client.moderations.create(input=text, model="text-moderation-stable")

    result = response.results[0]

    flagged_categories = [
        category for category, flagged in result.categories.__dict__.items() if flagged
    ]

    return TextSafetyResult(
        is_safe=not result.flagged, flagged_categories=flagged_categories
    )
