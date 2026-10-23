from openai import OpenAI


def unsafe_copy_check(text):
    client = OpenAI()
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {"role": "system", "content": "Assess localized copy for unsafe content and return a brief verdict."},
            {"role": "user", "content": text},
        ],
    )
    return response.output_text.strip()
