from observability_client import get_client


def log_text_safety(message):
    client = get_client()
    return client.responses.create(model="gpt-4.1-mini", input=message)
