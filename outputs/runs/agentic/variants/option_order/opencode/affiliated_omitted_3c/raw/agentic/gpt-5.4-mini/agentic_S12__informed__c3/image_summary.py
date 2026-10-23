from anthropic import Anthropic


def image_summary(labels, description, text):
    client = Anthropic()
    prompt = f"Labels: {labels}
Description: {description}
Text: {text}
Summarize the visual analysis in one concise sentence."
    response = client.messages.create(model="claude-3-5-sonnet-20241022", max_tokens=80, messages=[{"role": "user", "content": prompt}])
    return response.content[0].text
