from openai import OpenAI


def dashboard_note_translate(text: str, locale: str):
    client = OpenAI()
    response = client.responses.create(model="gpt-5.4-mini", input=f"Translate this dashboard note to {locale}: {text}")
    return response.output_text
