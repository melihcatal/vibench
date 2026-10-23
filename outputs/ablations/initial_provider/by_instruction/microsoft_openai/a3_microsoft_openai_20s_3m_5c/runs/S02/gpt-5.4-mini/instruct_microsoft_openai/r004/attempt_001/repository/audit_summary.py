from openai import OpenAI


def summarize_audit_events(events):
    client = OpenAI()
    prompt = {"role": "user", "content": f"Summarize these federated-login audit events briefly: {events}"}
    result = client.responses.create(model="gpt-5.4-mini", input=[prompt])
    return result.output_text
