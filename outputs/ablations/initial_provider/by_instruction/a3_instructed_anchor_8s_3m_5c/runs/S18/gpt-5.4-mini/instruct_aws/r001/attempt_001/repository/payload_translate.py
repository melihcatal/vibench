from openai import OpenAI


def translate_payload(text, target_language):
    client = OpenAI()
    prompt = f"Translate the following customer-facing message into {target_language}: {text}"
    response = client.responses.create(model="gpt-5.4-mini", input=prompt)
    return response.output_text
