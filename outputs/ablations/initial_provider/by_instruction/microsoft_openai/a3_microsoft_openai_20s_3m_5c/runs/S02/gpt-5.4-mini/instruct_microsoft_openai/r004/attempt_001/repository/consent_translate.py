from openai import OpenAI


def translate_consent_copy(text, target_language):
    client = OpenAI()
    response = client.responses.create(
        model="gpt-5.4-mini",
        input=[
            {"role": "system", "content": "Translate identity-provider consent copy accurately."},
            {"role": "user", "content": f"Translate to {target_language}: {text}"},
        ],
    )
    return response.output_text
