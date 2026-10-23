import openai


def invoice_note_translate(payload, config=None):
    config = config or {}
    client = openai.OpenAI(api_key=config.get("api_key"))
    model = config.get("translate_model", "gpt-4o-mini")
    source_language = payload.get("source_language", "auto")
    target_language = payload.get("target_language", "en")
    text = payload.get("text", "")
    response = client.responses.create(model=model, input=[{"role": "user", "content": f"Translate from {source_language} to {target_language}: {text}"}])
    return {"translation": response.output_text}
