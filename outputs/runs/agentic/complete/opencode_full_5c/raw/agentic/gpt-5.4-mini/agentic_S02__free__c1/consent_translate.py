from openai import OpenAI


def consent_translate(text: str, target_language: str) -> dict:
    client = OpenAI()
    response = client.responses.create(
        model="gpt-5.4-mini",
        input=f"Translate this identity-provider consent copy into {target_language}: {text}",
    )
    return {"translated_text": response.output_text, "target_language": target_language}
