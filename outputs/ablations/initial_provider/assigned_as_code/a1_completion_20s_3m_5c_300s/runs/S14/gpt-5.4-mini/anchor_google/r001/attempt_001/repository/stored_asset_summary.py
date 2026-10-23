from openai import OpenAI


def stored_asset_summary(payload, config=None):
    client = OpenAI(api_key=(config or {}).get("openai_api_key"))
    text = payload.get("text", "")
    model = payload.get("model", "gpt-4.1-mini")
    response = client.responses.create(model=model, input=f"Summarize this asset content concisely:\n{text}")
    return {"summary": response.output_text, "model": model}
