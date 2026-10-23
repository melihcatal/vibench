from openai import OpenAI


def script_translate(payload, config=None):
    config = config or {}
    client = OpenAI(api_key=config.get("openai_api_key"))
    response = client.responses.create(
        model=config.get("model", "gpt-5.4-mini"),
        input=payload["text"],
    )
    return {"translated_text": response.output_text}
