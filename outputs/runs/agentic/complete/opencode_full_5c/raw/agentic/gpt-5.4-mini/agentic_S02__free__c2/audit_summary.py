import os

import openai


def summarize_audit_events(events: list[dict]) -> str:
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    prompt = {
        "model": "gpt-5.4-mini",
        "input": f"Summarize these federated-login audit events: {events}",
    }
    response = client.responses.create(**prompt)
    return response.output_text
