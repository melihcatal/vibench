from openai import OpenAI


def localized_platform_output(text: str, locale: str) -> str:
    client = OpenAI()
    response = client.responses.create(
        model="gpt-4.1-mini", input=f"Translate the following text to {locale}: {text}"
    )
    return getattr(response, "output_text", "")
