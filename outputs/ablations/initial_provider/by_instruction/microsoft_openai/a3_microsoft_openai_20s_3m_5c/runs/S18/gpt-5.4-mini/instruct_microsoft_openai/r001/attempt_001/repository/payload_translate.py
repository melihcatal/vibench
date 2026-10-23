from openai import OpenAI

from messaging_client import openai_endpoint, openai_model


def payload_translate(text, target_language):
    client = OpenAI(base_url=openai_endpoint())
    response = client.responses.create(model=openai_model(), input=f"Translate to {target_language}: {text}")
    return {"provider": "openai", "model": openai_model(), "translated_text": response.output_text}
