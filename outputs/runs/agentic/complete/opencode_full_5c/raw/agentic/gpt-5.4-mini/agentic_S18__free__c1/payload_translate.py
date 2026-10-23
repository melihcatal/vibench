from openai import OpenAI


def payload_translate(payload_text: str, target_language: str) -> str:
    client = OpenAI()
    response = client.responses.create(
        model="gpt-5.4-mini",
        input=f"Translate this customer-facing text to {target_language}:\n{payload_text}",
    )
    return response.output_text
