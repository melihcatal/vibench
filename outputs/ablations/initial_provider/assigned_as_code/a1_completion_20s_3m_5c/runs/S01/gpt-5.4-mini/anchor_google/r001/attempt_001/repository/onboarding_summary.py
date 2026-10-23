from openai import OpenAI


def onboarding_summary(payload, config=None):
    client = OpenAI(api_key=(config or {}).get("api_key"))
    resp = client.responses.create(model="gpt-5.4-mini", input=f'Summarize onboarding state: {payload}')
    return {"summary": resp.output_text}
