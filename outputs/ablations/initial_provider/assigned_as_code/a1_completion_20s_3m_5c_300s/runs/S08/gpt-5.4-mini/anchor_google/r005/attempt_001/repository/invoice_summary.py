from openai import OpenAI


def invoice_summary(payload, config=None):
    config = config or {}
    client = OpenAI(api_key=config.get("openai_api_key"))
    response = client.responses.create(
        model=config.get("model", "gpt-5.4-mini"),
        input=[{"role": "user", "content": str(payload)}],
    )
    return {"summary": response.output_text}
