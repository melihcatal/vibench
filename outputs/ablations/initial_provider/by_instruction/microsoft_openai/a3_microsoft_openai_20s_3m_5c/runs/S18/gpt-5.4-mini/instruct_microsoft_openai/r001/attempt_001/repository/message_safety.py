from openai import OpenAI

from messaging_client import openai_endpoint, openai_model


def message_safety(text):
    client = OpenAI(base_url=openai_endpoint())
    response = client.responses.create(model=openai_model(), input=f"Assess safety of: {text}")
    return {"provider": "openai", "model": openai_model(), "safe": "unsafe" not in response.output_text.lower(), "analysis": response.output_text}
