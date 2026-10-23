from anthropic import Anthropic

anthropic_client = Anthropic(api_key='YOUR_ANTHROPIC_API_KEY')

def summarize_onboarding(text):
    response = anthropic_client.completions.create(
        model='claude-2',
        prompt=f'Summarize the following onboarding text: {text}',
        max_tokens_to_sample=100)
    return response.completion