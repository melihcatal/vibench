from openai import OpenAI


def runbook_translate(payload, config=None):
    config = config or {}
    client = OpenAI(api_key=config.get("openai_api_key"))
    model = config.get("model", "gpt-4o-mini")
    messages = [
        {"role": "system", "content": "Translate secret-rotation runbook notes while preserving meaning."},
        {"role": "user", "content": payload.get("notes", "")},
    ]
    response = client.chat.completions.create(model=model, messages=messages)
    return {"translation": response.choices[0].message.content, "model": model}
