from identity_client import openai_headers, post_json


def welcome_translate(text: str, locale: str):
    payload = {"model": "gpt-5.4-mini", "input": f"Translate to {locale}: {text}"}
    return post_json("https://api.openai.com/v1/responses", payload, headers=openai_headers())
