from openai import OpenAI


def vendor_text_safety(text):
    client = OpenAI()
    response = client.moderations.create(model="omni-moderation-latest", input=text)
    return response.results[0]
