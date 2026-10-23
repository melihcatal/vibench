from openai import OpenAI

client = OpenAI()

def moderate_claims(text: str) -> bool:
    response = client.moderations.create(model='omni-moderation-latest', input=text)
    return not any(item.flagged for item in response.results)
