from openai import OpenAI


def unsafe_copy_check(text: str, locale: str | None = None) -> str:
    client = OpenAI()
    response = client.responses.create(
        model="gpt-5.4-mini",
        input=[
            {"role": "system", "content": "Check localized copy for unsafe content and return a brief verdict."},
            {"role": "user", "content": text},
        ],
    )
    return response.output_text
