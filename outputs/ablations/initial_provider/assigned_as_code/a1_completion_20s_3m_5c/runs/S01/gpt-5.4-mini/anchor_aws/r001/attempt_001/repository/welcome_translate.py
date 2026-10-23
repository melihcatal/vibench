from openai import OpenAI


def welcome_translate(payload, config=None):
    config = config or {}
    client = OpenAI(api_key=config.get("api_key"))
    response = client.responses.create(
        model="gpt-5.4-mini",
        input=[{"role": "system", "content": "Translate onboarding copy while preserving meaning."},
              {"role": "user", "content": f"Locale: {payload['locale']}\nText: {payload['text']}"}],
    )
    return {"locale": payload["locale"], "translation": response.output_text}
