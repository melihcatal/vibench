import json

from openai import OpenAI


def image_summary(payload, config=None):
    config = config or {}
    client = OpenAI()
    model = config.get("model", "gpt-5.4-mini")
    text = json.dumps(payload, sort_keys=True)
    response = client.responses.create(model=model, input=f"Summarize these visual analysis results briefly: {text}")
    return {"summary": response.output_text}
