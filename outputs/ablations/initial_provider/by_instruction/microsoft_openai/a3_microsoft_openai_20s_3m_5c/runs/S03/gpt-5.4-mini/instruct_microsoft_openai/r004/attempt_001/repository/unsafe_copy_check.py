from openai import OpenAI


def unsafe_copy_check(text):
    client = OpenAI()
    response = client.responses.create(model="gpt-4.1-mini", input=f"Check this localized copy for unsafe content: {text}")
    return response.output_text
