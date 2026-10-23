from openai import OpenAI


def visual_safety_text(text: str) -> str:
    client = OpenAI()
    response = client.responses.create(model="gpt-5.4-mini", input=f"Check this image label text for unsafe content and respond briefly: {text}")
    return response.output_text
