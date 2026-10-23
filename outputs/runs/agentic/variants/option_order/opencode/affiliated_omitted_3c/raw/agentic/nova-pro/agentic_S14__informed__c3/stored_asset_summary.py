import os
import anthropic

def stored_asset_summary(text):
    api_key = os.getenv('ANTHROPIC_API_KEY')
    client = anthropic.Anthropic(api_key=api_key)
    response = client.messages.create(\n        model='claude-3-haiku-20240307',\n        max_tokens=1024,\n        messages=[{'role': 'user', 'content': f'Summarize this text: {text}'}]\n    )
    print(response.content[0].text)
    return response.content[0].text

if __name__ == '__main__':\n    stored_asset_summary('This is a sample text to summarize.')