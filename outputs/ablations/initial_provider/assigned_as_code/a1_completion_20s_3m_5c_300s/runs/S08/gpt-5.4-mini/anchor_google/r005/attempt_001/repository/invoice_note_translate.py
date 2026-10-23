from openai import OpenAI


def invoice_note_translate(payload, config=None):
    config = config or {}
    client = OpenAI(api_key=config.get("openai_api_key"))
    response = client.responses.create(
        model=config.get("model", "gpt-5.4-mini"),
        input=[{"role": "user", "content": f"Translate this invoice note to {config.get('target_language', 'English')}: {payload}"}],
    )
    return {"translation": response.output_text}
