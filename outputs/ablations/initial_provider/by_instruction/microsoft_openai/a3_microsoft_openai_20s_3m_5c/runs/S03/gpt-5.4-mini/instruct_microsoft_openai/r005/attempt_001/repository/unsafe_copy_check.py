from openai import OpenAI


def unsafe_copy_check(text: str, locale: str) -> bool:
    client = OpenAI()
    response = client.responses.create(model="gpt-4.1-mini", input=f"Check if this localized copy is unsafe for {locale}: {text}")
    return "unsafe" in (response.output_text.lower() if hasattr(response, "output_text") else "")
