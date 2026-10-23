from openai import OpenAI


def invoice_note_translate(text, target_language="en"):
    client = OpenAI()
    response = client.responses.create(
        model="gpt-5.4-mini",
        input=[
            {"role": "system", "content": f"Translate invoice notes to {target_language}."},
            {"role": "user", "content": text},
        ],
    )
    return response.output_text
