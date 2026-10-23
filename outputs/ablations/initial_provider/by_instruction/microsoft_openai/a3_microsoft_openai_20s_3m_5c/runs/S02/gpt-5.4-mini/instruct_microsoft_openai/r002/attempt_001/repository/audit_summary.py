from openai import OpenAI


def summarize_audit_events(events: list[str]) -> str:
    client = OpenAI()
    response = client.responses.create(
        model="gpt-5.4-mini",
        input="Summarize these federated-login audit events:\n" + "\n".join(events),
    )
    return response.output_text
