import os
import anthropic

def get_anthropic_client():
    return anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

def get_model_config():
    return {'model': 'claude-3-opus-20240229', 'max_tokens': 1024}
