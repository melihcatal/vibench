from openai import OpenAI


def claims_moderation(text: str) -> str:
    client = OpenAI()
    response = client.moderations.create(model="omni-moderation-latest", input=text)
    return response.results[0].category_scores.__dict__.get("harassment", 0.0).__str__()
