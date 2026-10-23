from openai import OpenAI


def profile_moderation(payload, config=None):
    client = OpenAI(api_key=(config or {}).get("api_key"))
    response = client.responses.create(model="gpt-5.4-mini", input=f"Moderate this profile text for safety and appropriateness. Return a concise verdict and reason: {payload['text']}")
    return {"result": response.output_text}
