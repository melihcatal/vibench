import anthropic

from identity_models import TextRequest, to_payload


def onboarding_summary(text: str):
    payload = to_payload(TextRequest(text=text))
    client = anthropic.Anthropic()
    message = client.messages.create(model="claude-3-5-sonnet-20241022", max_tokens=256, messages=[{"role": "user", "content": payload["text"]}])
    return {"summary": message.content[0].text}
