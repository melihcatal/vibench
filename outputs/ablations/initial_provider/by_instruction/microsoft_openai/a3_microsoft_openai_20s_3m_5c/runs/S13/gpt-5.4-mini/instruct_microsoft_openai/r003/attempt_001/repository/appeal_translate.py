from openai import OpenAI


def appeal_translate(text: str, target_language: str = "en"):
    client = OpenAI()
    return client.responses.create(model="gpt-5.4-mini", input=f"Translate appeal text to {target_language}: {text}")
