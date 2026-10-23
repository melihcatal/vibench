from anthropic import Anthropic


def onboarding_summary(payload, config=None):
    client = Anthropic(api_key=(config or {}).get("api_key"))
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=256,
        messages=[{"role": "user", "content": payload["text"]}],
    )
    return {"summary": message.content[0].text}
