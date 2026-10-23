import anthropic

from identity_models import FederatedProfile


client = anthropic.Anthropic()


def summarize_audit_events(events: list[dict]) -> str:
    prompt = f"Summarize these federated-login audit events for compliance review: {events}"
    message = client.messages.create(model='claude-3-5-sonnet-20241022', max_tokens=256, messages=[{'role': 'user', 'content': prompt}])
    return message.content[0].text
