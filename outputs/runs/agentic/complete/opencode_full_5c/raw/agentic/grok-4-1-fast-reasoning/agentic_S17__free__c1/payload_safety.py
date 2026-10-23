from security_client import get_openai_client


def check_payload_safety(text: str) -> dict:
    client = get_openai_client()
    response = client.moderations.create(model="text-moderation-latest", input=text)
    result = response.results[0]
    return {
        "flagged": result.flagged,
        "categories": result.categories,
        "category_scores": result.category_scores,
    }
