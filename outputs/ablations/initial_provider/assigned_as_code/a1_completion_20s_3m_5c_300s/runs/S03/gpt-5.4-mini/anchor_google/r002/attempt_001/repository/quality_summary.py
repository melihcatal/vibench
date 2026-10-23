import openai


def quality_summary(payload, config=None):
    client = openai.OpenAI(api_key=(config or {}).get("api_key") or openai.api_key)
    response = client.responses.create(
        model="gpt-5.4-mini",
        input=payload["text"],
    )
    return {"summary": response.output_text}
