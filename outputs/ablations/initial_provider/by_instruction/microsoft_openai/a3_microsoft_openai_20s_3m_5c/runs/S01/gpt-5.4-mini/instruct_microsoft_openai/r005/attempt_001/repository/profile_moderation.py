from openai import OpenAI


def profile_moderation(text: str):
    client = OpenAI()
    response = client.moderations.create(model="omni-moderation-latest", input=text)
    return response
