from openai import OpenAI


def rotation_summary(payload, config=None):
    client = OpenAI(api_key=(config or {}).get("api_key"))
    text = payload["notes"]
    result = client.responses.create(model="gpt-5.4-mini", input=f"Summarize secret rotation status:\n{text}")
    return {"summary": result.output_text}
