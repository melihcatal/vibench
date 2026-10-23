from openai import OpenAI


def vendor_text_safety(text):
    client = OpenAI(api_key=None)
    return client.moderations.create(model="omni-moderation-latest", input=text)
