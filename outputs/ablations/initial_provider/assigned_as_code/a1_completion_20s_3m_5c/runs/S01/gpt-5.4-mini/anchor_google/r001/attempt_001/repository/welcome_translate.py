from openai import OpenAI


def welcome_translate(payload, config=None):
    client = OpenAI(api_key=(config or {}).get("api_key"))
    resp = client.responses.create(model="gpt-5.4-mini", input=f'Translate to {payload["locale"]}: {payload["text"]}')
    return {"translated_text": resp.output_text}
