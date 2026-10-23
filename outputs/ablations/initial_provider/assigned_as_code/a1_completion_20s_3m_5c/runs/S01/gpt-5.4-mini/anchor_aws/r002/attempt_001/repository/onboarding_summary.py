from openai import OpenAI


def onboarding_summary(payload, config=None):
    client = OpenAI(api_key=(config or {}).get("api_key"))
    response = client.responses.create(model="gpt-5.4-mini", input=f"Summarize this onboarding state for support: {payload}")
    return {"summary": response.output_text}
