from openai import OpenAI


def vendor_text_safety(text):
    client = OpenAI()
    result = client.moderations.create(model="omni-moderation-latest", input=text)
    return result.results[0].model_dump()
