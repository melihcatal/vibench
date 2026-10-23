from openai import OpenAI


def check_text_safety(text):
    client = OpenAI()
    response = client.responses.create(
        model="gpt-5.4-mini",
        input=[
            {"role": "system", "content": "Assess user-generated document fields for unsafe content."},
            {"role": "user", "content": str(text)},
        ],
    )
    return response.output_text
