import os
from openai import OpenAI

_PROVIDER_MODEL = os.getenv("OPENAI_SAFETY_MODEL", "gpt-4o-mini")


def unsafe_copy_check(text: str, locale: str) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY")) if os.getenv("OPENAI_API_KEY") else OpenAI()
    prompt = f'Check this localized copy for unsafe content in locale {locale}. Return a short risk assessment. Copy: {text}'
    response = client.responses.create(model=_PROVIDER_MODEL, input=prompt)
    output_text = getattr(response, "output_text", None)
    if not output_text:
        output_text = response.output[0].content[0].text
    return output_text.strip()
