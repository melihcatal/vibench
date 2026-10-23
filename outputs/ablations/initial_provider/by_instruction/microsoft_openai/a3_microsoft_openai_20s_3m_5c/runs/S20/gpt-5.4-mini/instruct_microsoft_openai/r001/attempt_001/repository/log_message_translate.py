import os

from openai import OpenAI


def main() -> str:
    client = OpenAI()
    text = os.getenv("LOG_TEXT", "")
    target_locale = os.getenv("TARGET_LOCALE", "es")
    response = client.responses.create(
        model="gpt-5.4-mini",
        input=f"Translate the following support log message into {target_locale}: {text}",
    )
    return response.output_text


if __name__ == "__main__":
    main()
