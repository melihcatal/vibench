from openai import OpenAI


def translate_consent(text: str, target_language: str):
    client = OpenAI()
    response = client.responses.create(
        model="gpt-5.4-mini",
        input=f"Translate this identity-provider consent copy into {target_language}: {text}",
    )
    return response.output_text
