from anthropic import Anthropic

client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

def stored_asset_summary(text):
    response = client.completions.create(
        model='claude-2.1',
        prompt=f'Summarize the following text: {text}',
        max_tokens_to_sample=1024
    )
    return response.completion