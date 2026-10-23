import os
import requests
from safety_models import ModerationRequest
from safety_client import SafetyClient
from typing import List

# Use AWS SDK to synthesize speech via Amazon Polly
import boto3

# Polly client from boto3 (AWS) configured via env vars: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
polly_client = boto3.client('polly', region_name=os.getenv('AWS_REGION', 'us-east-1'))


def generate_brief_audio(moderation_request: ModerationRequest, output_format: str = 'mp3') -> bytes:
    """Generate a spoken brief summarising moderation decisions for a single text.
    Returns the raw audio bytes.
    """
    client = SafetyClient()
    response = client.check_content(moderation_request)

    # Build a short spoken script such as:
    # "The text was flagged for hate with high severity. It contains unsafe spans ..."
    parts = []
    if any(f.severity >= f.WARNING for f in response.flags):
        parts.append('The content violates policy.')
        for f in response.flags:
            if f.severity >= f.WARNING:
                parts.append(f"Specifically, it was flagged for {f.category} with {f.severity.name.lower()} severity.")
    else:
        parts.append('The content is safe.')
    script = ' '.join(parts) + ' End of brief.'

    # Polly synthesis parameters
    synthesis_input = {
        'Text': script,
        'TextType': 'text',
        'OutputFormat': output_format,
        'VoiceId': 'Joanna'  # or any preferred voice
    }
    response = polly_client.synthesize_speech(**synthesis_input)
    # For streaming responses, check if response['AudioStream'] is available
    if hasattr(response, 'AudioStream'):
        return response['AudioStream'].read()
    # Otherwise return binary content directly
    return response.get('AudioStream', b'').read()

# Example execution (run locally)
if __name__ == '__main__':
    txt = 'This is a hateful message.'
    brief = generate_brief_audio(ModerationRequest(txt))
    # Write to a file for listening
    with open('moderation_brief.mp3', 'wb') as f:
        f.write(brief)
    print('Audio brief written to moderation_brief.mp3')
