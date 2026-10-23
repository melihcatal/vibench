from openai import OpenAI

PROVIDER = "openai:gpt-4.1-mini"


def check_unsafe_copy(localized_text: str, locale: str) -> dict:
    client = OpenAI()
    prompt = (
        f"Assess whether this localized copy for locale={locale} contains unsafe, hateful, self-harm, "
        f"or policy-violating content. Text: {localized_text}\nReturn JSON with unsafe and findings."
    )
    response = client.responses.create(model="gpt-4.1-mini", input=prompt)
    output = getattr(response, "output_text", "")
    return {"unsafe": bool(output), "findings": [output[:120]] if output else [], "provider": PROVIDER}
