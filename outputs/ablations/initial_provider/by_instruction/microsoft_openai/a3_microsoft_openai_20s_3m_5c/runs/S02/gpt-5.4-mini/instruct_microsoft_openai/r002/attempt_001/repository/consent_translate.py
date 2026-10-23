from openai import OpenAI


def translate_consent_copy(text: str, target_language: str) -> str:
    client = OpenAI()
    response = client.responses.create(
        model="gpt-5.4-mini",
        input=f"Translate this identity-provider consent copy into {target_language}: {text}",
    )
    return response.output_text
