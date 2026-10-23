import os
from openai import OpenAI


def translate(text: str, locale: str) -> str:
    client = OpenAI()
    resp = client.responses.create(
        model="gpt-5.4-mini",
        input=f"Translate this support log message to {locale}: {text}",
    )
    return resp.output_text


if __name__ == "__main__":
    print(translate(os.getenv("LOG_TEXT", ""), os.getenv("LOCALE", "es")))
