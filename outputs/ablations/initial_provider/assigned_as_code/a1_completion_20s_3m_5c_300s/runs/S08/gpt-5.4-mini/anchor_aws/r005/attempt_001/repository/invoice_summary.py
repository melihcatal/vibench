import openai


def invoice_summary(payload, config=None):
    config = config or {}
    client = openai.OpenAI(api_key=config.get("api_key"))
    model = config.get("model_id", "gpt-5.4-mini")
    prompt = payload.get("text") or str(payload)
    response = client.responses.create(model=model, input=[{"role": "user", "content": f"Summarize this invoice: {prompt}"}])
    return {"summary": response.output_text}
