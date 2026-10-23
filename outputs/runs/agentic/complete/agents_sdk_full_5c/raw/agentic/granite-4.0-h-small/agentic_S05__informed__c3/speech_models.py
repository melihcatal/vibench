import json

# Mapping of provider names to model identifiers
MODEL_MAP = {
    'google': {
        'model': 'default',               # Default streaming model for Google
        'language_code': 'en-US',
    },
    'amazon': {
        'model': 'general',               # General purpose model for Amazon Transcribe
        'language_code': 'en-US',
    },
    'azure': {
        'model': 'default',               # Default model for Azure Speech
        'language_code': 'en-US',
    },
    'watson': {
        'model': 'broad',                 # Broadband model for Watson STT
        'language_code': 'en-US',
    },
    'deepgram': {
        'model': 'nova',                  # Nova model for Deepgram streaming API
        'language_code': 'en-US',
    },
}

def get_model_config(provider='google'):
    """Return a dict with model identifier and language code for a provider."""
    cfg = MODEL_MAP.get(provider.lower())
    if not cfg:
        raise ValueError(f'Unsupported provider: {provider}')
    return cfg

# Helper to normalize language codes to provider-specific formats if needed

def normalize_language(provider, language_code):
    # Some providers expect BCP-47 tags, others expect short codes; implement mapping if needed
    return language_code

if __name__ == '__main__':
    # Example usage
    cfg = get_model_config('amazon')
    print('Selected model:', cfg)
