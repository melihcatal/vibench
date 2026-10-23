from openai import OpenAI


def onboarding_summary(payload, config=None):
    config = config or {}
    client = OpenAI(api_key=config.get("openai_api_key"))
    prompt = payload["state"]
    response = client.responses.create(model="gpt-5.4-mini", input=prompt)
    return {"summary": response.output_text}
