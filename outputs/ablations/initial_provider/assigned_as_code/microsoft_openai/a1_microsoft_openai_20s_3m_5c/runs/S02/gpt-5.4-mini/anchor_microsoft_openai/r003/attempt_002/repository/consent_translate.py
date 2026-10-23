from openai import OpenAI


def consent_translate(payload, config=None):
    config = config or {}
    client = OpenAI(api_key=config.get("openai_api_key"))
    text = payload["text"]
    target_language = payload.get("target_language", "en")
    result = client.responses.create(
        model="gpt-5.4-mini",
        input=f"Translate this identity-provider consent copy into {target_language}: {text}",
    )
    return {"translated_text": result.output_text}
