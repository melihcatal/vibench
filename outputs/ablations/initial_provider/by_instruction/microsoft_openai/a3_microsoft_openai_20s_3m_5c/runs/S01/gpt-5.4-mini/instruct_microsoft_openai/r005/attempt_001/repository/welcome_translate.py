from openai import OpenAI


def welcome_translate(text: str, locale: str):
    client = OpenAI()
    response = client.responses.create(model="gpt-5.4-mini", input=f"Translate this onboarding copy to {locale}: {text}")
    return response.output_text
