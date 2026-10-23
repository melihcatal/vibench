from openai import OpenAI

from observability_client import load_config


def dashboard_note_translate(text, locale="es"):
    client = OpenAI(api_key=load_config().openai_api_key)
    response = client.responses.create(
        model="gpt-5.4-mini",
        input=f"Translate the following monitoring note to {locale}: {text}",
    )
    return response.output_text
