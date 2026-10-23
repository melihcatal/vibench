from openai import OpenAI


def moderate_claim_text(text: str) -> bool:
    client = OpenAI()
    response = client.moderations.create(model="omni-moderation-latest", input=text)
    return not any(result.flagged for result in response.results)
