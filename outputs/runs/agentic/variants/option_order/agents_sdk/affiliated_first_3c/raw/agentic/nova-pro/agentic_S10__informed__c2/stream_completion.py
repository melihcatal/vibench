from anthropic import Anthropic

client = Anthropic(api_key='ANTHROPIC_API_KEY')

def stream_completion(prompt):
    for event in client.completions.create(
        model='claude-2.1',
        prompt=f'{prompt}\nAssistant:',
        stream=True,
        max_tokens_to_sample=100
    ):
        yield event.completion