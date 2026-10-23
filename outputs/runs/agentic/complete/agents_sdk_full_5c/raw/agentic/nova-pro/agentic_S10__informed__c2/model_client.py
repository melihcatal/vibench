import os

def get_api_key(provider):
    if provider == 'dashscope':
        return os.getenv('DASHSCOPE_API_KEY')
    elif provider == 'openai':
        return os.getenv('OPENAI_API_KEY')
    elif provider == 'anthropic':
        return os.getenv('ANTHROPIC_API_KEY')
    elif provider == 'mistral':
        return os.getenv('MISTRAL_API_KEY')
    else:
        raise ValueError('Unsupported provider')