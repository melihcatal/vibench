from openai import OpenAI


def onboarding_summary(payload, config=None):
    client = OpenAI(api_key=(config or {}).get("api_key"))
    response = client.responses.create(
        model=(config or {}).get("model", "gpt-5.4-mini"),
        input=[
            {"role": "system", "content": "Summarize onboarding state for support."},
            {"role": "user", "content": payload["state"]},
        ],
    )
    return {"summary": response.output_text}
