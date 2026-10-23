import openai


def consent_translate(payload, config=None):
    client = openai.OpenAI(api_key=(config or {}).get("openai_api_key"))
    response = client.responses.create(model="gpt-5.4-mini", input=f"Translate this identity-provider consent copy to {payload['target_language']}: {payload['text']}")
    return {"translated_text": response.output_text}
