from openai import OpenAI


def consent_translate(payload, config=None):
    config = config or {}
    client = OpenAI(api_key=config.get("openai_api_key"))
    response = client.responses.create(
        model="gpt-5.4-mini",
        input=f"Translate consent copy into {payload['target_language']}: {payload['text']}",
    )
    return {"translation": response.output_text, "provider": "openai"}
