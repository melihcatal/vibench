from openai import OpenAI


def check_message_safety(text):
    client = OpenAI()
    response = client.moderations.create(model="omni-moderation-latest", input=text)
    return response.results[0].model_dump()
