from openai import OpenAI


def check_ocr_safety(text: str) -> dict:
    client = OpenAI()
    response = client.moderations.create(model="omni-moderation-latest", input=text)
    return response.model_dump()
