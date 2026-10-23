from anthropic import Anthropic

MODEL = "claude-3-5-sonnet-20241022"


def moderation_summary(decisions):
    client = Anthropic(api_key=None)
    prompt = f"Summarize these moderation decisions for an operations reviewer: {decisions}"
    response = client.messages.create(model=MODEL, max_tokens=256, messages=[{"role": "user", "content": prompt}])
    return response.content[0].text
