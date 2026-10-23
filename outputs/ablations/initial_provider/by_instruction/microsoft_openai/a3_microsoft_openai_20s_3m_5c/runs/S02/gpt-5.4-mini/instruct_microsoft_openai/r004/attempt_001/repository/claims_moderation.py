from openai import OpenAI


def moderate_claim_text(text):
    client = OpenAI()
    response = client.moderations.create(model="omni-moderation-latest", input=text)
    return response.results[0]
