from openai import OpenAI


def moderate_transcript(text: str) -> dict:
    client = OpenAI()
    response = client.moderations.create(model="omni-moderation-latest", input=text)
    result = response.results[0]
    return {
        "flagged": result.flagged,
        "categories": dict(result.categories),
        "category_scores": dict(result.category_scores),
    }
