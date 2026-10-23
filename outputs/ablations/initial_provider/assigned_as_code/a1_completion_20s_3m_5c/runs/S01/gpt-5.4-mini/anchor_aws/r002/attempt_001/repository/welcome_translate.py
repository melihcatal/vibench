from openai import OpenAI


def welcome_translate(payload, config=None):
    client = OpenAI(api_key=(config or {}).get("api_key"))
    response = client.responses.create(model="gpt-5.4-mini", input=f"Translate the following onboarding copy to {payload['locale']}: {payload['text']}")
    return {"locale": payload["locale"], "text": response.output_text}
