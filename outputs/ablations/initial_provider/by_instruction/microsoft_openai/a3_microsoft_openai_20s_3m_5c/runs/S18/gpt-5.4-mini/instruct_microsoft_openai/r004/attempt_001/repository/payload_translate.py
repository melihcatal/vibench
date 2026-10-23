from openai import OpenAI


def payload_translate(payload_text, target_language="en"):
    client = OpenAI()
    prompt = f"Translate to {target_language}: {payload_text}"
    result = client.responses.create(model="gpt-5.4-mini", input=prompt)
    return getattr(result, "output_text", payload_text)
