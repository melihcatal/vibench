from identity_client import IdentityClient


def welcome_translate(text: str, locale: str):
    client = IdentityClient.from_env()
    return client.post("/chat/completions", {"model": "gpt-5.4-mini", "messages": [{"text": text, "locale": locale}]})
