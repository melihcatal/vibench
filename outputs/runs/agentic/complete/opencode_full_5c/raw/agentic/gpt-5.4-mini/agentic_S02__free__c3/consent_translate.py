from openai import OpenAI


def translate_consent_copy(text: str, target_language: str) -> dict:
    client = OpenAI()
    response = client.responses.create(
        model="gpt-5.4-mini", input=f"Translate to {target_language}: {text}"
    )
    return {"language": target_language, "translation": response.output_text}
