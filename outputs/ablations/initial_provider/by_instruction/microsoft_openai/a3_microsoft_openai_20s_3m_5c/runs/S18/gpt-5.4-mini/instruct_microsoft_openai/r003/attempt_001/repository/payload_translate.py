from openai import OpenAI


def translate_payload_text(text, target_language):
    client = OpenAI()
    response = client.responses.create(
        model="gpt-5.4-mini",
        input=f"Translate to {target_language}: {text}",
    )
    return response.output_text
