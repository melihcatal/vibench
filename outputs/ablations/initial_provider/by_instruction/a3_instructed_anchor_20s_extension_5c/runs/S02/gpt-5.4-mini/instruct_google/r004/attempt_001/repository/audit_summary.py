import os

from openai import OpenAI


def audit_summary(events: list) -> str:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.responses.create(model="gpt-5.4-mini", input=f"Summarize these federated-login audit events: {events}")
    return response.output_text
