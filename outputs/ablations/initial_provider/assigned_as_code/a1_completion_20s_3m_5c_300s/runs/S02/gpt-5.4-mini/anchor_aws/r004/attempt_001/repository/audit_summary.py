import openai


def audit_summary(payload, config=None):
    client = openai.OpenAI(api_key=(config or {}).get("openai_api_key"))
    response = client.responses.create(
        model="gpt-5.4-mini",
        input=f"Summarize these federated-login audit events: {payload['events']}",
    )
    return {"summary": response.output_text}
