from openai import OpenAI

from identity_client import openai_api_key
from identity_models import TranslationRequest


def welcome_translate(text: str, locale: str):
    req = TranslationRequest(text=text, locale=locale)
    client = OpenAI(api_key=openai_api_key())
    response = client.responses.create(
        model="gpt-5.4-mini",
        input=f"Translate to {req.locale}: {req.text}",
    )
    return response.output_text
