from speech_client import get_client


def moderate_transcript(text: str):
    client = get_client()
    result = client.moderations.create(
        model="omni-moderation-latest",
        input=text,
    )
    return {
        "flagged": result.results[0].flagged,
        "categories": result.results[0].categories.model_dump(),
        "category_scores": result.results[0].category_scores.model_dump(),
        "raw": result.model_dump(),
    }
