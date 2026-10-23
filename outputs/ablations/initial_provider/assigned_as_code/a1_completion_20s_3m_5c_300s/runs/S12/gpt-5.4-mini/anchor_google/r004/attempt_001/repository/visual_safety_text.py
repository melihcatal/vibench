from openai import OpenAI


def visual_safety_text(payload, config=None):
    config = config or {}
    client = OpenAI()
    model = config.get("model", "gpt-5.4-mini")
    text = payload.get("labels", [])
    response = client.responses.create(model=model, input=f"Assess whether these visual labels contain unsafe text: {text}")
    return {"assessment": response.output_text}
