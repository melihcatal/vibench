from openai import OpenAI


def unsafe_copy_check(text, model="gpt-5.4-mini"):
    client = OpenAI()
    response = client.responses.create(
        model=model,
        input=f"Check localized copy for unsafe content: {text}",
    )
    return response.output_text
