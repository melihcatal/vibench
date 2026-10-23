from openai import OpenAI


def audit_summary(payload, config=None):
    config = config or {}
    client = OpenAI(api_key=config.get("openai_api_key"))
    prompt = payload.get("events", [])
    response = client.responses.create(model="gpt-5.4-mini", input=str(prompt))
    return {"summary": response.output_text, "provider": "openai"}
