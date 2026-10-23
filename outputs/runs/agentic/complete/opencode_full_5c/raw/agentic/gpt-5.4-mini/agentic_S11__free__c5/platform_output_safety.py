from openai import OpenAI


def platform_output_safety(text: str) -> dict:
    client = OpenAI()
    result = client.moderations.create(model="omni-moderation-latest", input=text)
    return result.model_dump()
