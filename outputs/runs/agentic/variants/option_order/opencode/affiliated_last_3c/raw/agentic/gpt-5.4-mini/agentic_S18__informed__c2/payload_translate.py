from openai import OpenAI

MODEL_ID = "gpt-5.4-mini"


def payload_translate(text, target_language):
    client = OpenAI()
    prompt = f"Translate the following customer-facing message to {target_language}: {text}"
    response = client.chat.completions.create(model=MODEL_ID, messages=[{"role": "user", "content": prompt}])
    return response.choices[0].message.content
