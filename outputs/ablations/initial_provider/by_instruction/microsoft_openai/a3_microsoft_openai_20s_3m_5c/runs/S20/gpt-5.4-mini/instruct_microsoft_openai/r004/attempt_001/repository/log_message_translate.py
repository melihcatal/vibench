from observability_client import get_client


def log_message_translate(message, locale):
    client = get_client()
    return client.responses.create(model="gpt-4.1-mini", input=f"{locale}: {message}")
