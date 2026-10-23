from openai import OpenAI


def summarize_audit(events):
    client = OpenAI()
    prompt = "Summarize these federated-login audit events concisely: " + repr(events)
    response = client.responses.create(model="gpt-5.4-mini", input=prompt)
    return response.output_text
