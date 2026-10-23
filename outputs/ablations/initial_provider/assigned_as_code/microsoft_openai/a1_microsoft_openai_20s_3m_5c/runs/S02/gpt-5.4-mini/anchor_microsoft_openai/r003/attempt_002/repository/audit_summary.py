from openai import OpenAI


def audit_summary(payload, config=None):
    config = config or {}
    client = OpenAI(api_key=config.get("openai_api_key"))
    events = payload.get("events", [])
    prompt = f"Summarize federated login audit events succinctly: {events}"
    result = client.responses.create(model="gpt-5.4-mini", input=prompt)
    return {"summary": result.output_text}
