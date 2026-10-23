from anthropic import Anthropic

ANTHROPIC_API_KEY = 'your_anthropic_api_key'

def summarize_moderation(decisions):
    client = Anthropic(api_key=ANTHROPIC_API_KEY)
    prompt = f'Summarize the following moderation decisions: {decisions}'
    response = client.messages.create(model='claude-3-opus-20240229', max_tokens=1024, prompt=prompt)
    return response.content