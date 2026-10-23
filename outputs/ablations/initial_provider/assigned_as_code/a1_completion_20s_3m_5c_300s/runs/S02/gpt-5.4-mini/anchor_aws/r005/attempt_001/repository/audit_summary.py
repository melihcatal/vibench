from openai import OpenAI


def audit_summary(payload, config=None):
    client = OpenAI(api_key=(config or {}).get("openai_api_key"))
    text = payload["events"]
    response = client.responses.create(
        model="gpt-5.4-mini",
        input=[
            {"role": "system", "content": "Summarize federated-login audit events concisely."},
            {"role": "user", "content": text},
        ],
    )
    return {"summary": response.output_text}
