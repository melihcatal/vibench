from openai import OpenAI

from model_client import create_platform_client


# Provider-identifying signal: OpenAI moderation model omni-moderation-latest.
def check_platform_output_for_unsafe_content(output_text: str) -> dict:
    client: OpenAI = create_platform_client()
    result = client.moderations.create(
        model="omni-moderation-latest",
        input=output_text,
    )
    first = result.results[0]
    return {
        "flagged": first.flagged,
        "categories": first.categories.model_dump() if hasattr(first.categories, "model_dump") else dict(first.categories),
        "category_scores": first.category_scores.model_dump() if hasattr(first.category_scores, "model_dump") else dict(first.category_scores),
        "provider": "openai",
    }
