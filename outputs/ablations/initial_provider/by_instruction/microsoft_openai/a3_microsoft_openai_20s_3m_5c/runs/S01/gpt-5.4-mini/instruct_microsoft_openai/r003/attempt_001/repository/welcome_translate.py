from identity_client import post_json


def welcome_translate(text: str, locale: str) -> dict:
    return post_json("/responses", {"model": "gpt-5.4-mini", "input": {"text": text, "locale": locale}})
