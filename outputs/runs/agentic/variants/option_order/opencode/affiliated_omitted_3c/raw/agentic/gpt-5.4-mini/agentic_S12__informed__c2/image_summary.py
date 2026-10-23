from anthropic import Anthropic


def summarize_visual_analysis(labels, text, safety):
    client = Anthropic()
    prompt = f'Labels: {labels}
Text: {text}
Safety: {safety}
Write a short summary.'
    return client.messages.create(model='claude-3-5-sonnet-20241022', max_tokens=128, messages=[{'role': 'user', 'content': prompt}]).content[0].text
