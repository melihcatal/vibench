import anthropic


def profile_moderation(payload, config=None):
    client = anthropic.Anthropic(api_key=(config or {}).get("api_key"))
    msg = client.messages.create(model="claude-3-5-sonnet-latest", max_tokens=64, messages=[{"role": "user", "content": payload["text"]}])
    return {"moderation_result": msg.content[0].text}
