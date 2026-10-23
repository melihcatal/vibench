from openai import OpenAI


def translate_message(text: str, locale: str) -> str:
    client = OpenAI()
    response = client.responses.create(model="gpt-5.4-mini", input=[{"role": "system", "content": f"Translate the message to {locale}."}, {"role": "user", "content": text}])
    return response.output_text
