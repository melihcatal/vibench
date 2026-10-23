from openai import OpenAI


def translate_record_text(text, target_language):
    client = OpenAI()
    response = client.responses.create(
        model="gpt-5.4-mini",
        input=[
            {"role": "system", "content": "Translate user-facing document fields."},
            {"role": "user", "content": f"Translate to {target_language}: {text}"},
        ],
    )
    return response.output_text
