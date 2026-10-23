import os

# Simple configuration loader for credentials
CREDENTIALS = {
    # Textract credentials are expected as environment variables per AWS SDK
    # No explicit client creation here; callers use boto3 directly.

    # Mindee Invoice OCR API key
    'MINDEE_API_KEY': os.getenv('MINDEE_API_KEY'),
    # Anthropic Chat model ID (example identifier)
    'ANTHROPIC_MODEL_ID': os.getenv('ANTHROPIC_MODEL_ID', 'claude-3-haiku-20240307'),
    # Perspective API key
    'PERSPECTIVE_API_KEY': os.getenv('PERSPECTIVE_API_KEY'),
}

def get_api_key(provider):
    return CREDENTIALS.get(f'{provider.upper().replace(" ", "_")}_API_KEY')
