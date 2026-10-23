from openai import OpenAI


def translate_live_caption(text: str, target_language: str = "es") -> str:
    client = OpenAI()
    response = client.responses.create(
        model="gpt-5.4-mini",
        input=f"Translate the following live caption to {target_language}: {text}",
    )
    return response.output_text
