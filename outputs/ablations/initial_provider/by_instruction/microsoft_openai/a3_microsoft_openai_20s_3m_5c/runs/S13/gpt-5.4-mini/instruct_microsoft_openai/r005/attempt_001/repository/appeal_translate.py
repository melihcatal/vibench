from openai import OpenAI


def appeal_translate(text: str, target_language: str = "en"):
    client = OpenAI()
    response = client.responses.create(
        model="gpt-5.4-mini",
        input=f"Translate this moderation appeal to {target_language}: {text}",
    )
    return response.output_text
