from openai import OpenAI


def alt_text_translate(payload, config=None):
    config = config or {}
    client = OpenAI()
    model = config.get("model", "gpt-5.4-mini")
    target_language = config.get("target_language", "Spanish")
    text = payload.get("description", "")
    response = client.responses.create(model=model, input=f"Translate this image description into {target_language}: {text}")
    return {"translated_text": response.output_text}
