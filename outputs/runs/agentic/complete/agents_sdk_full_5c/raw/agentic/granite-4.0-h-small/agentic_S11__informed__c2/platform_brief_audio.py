import os
from model_client import ManagedModelClient
from model_models import RequestPayload, ResponseWrapper
import requests

def generate_speech(text: str, voice: str = 'en-US-JennyNeural') -> bytes:
    """Generate spoken audio from text using Azure Speech Service.
    Returns raw audio bytes.
    """
    endpoint = os.getenv('AZURE_SPEECH_ENDPOINT') + "/synthesize"
    headers = {
        "Authorization": f"Bearer {os.getenv('AZURE_SPEECH_KEY')}",
        "Content-Type": "application/ssml+xml",
        "X-Microsoft-OutputFormat": "audio-16khz-64kbitrate-mono-mp3"
    }
    ssml = f"<speak version='1.0'><voice name='{voice}'>{text}</voice></speak>"
    resp = requests.post(endpoint, data=ssml.encode('utf-8'), headers=headers)
    resp.raise_for_status()
    return resp.content

# Helper that returns audio bytes plus provider metadata
client = ManagedModelClient(provider='huggingface', token=os.getenv('HF_TOKEN'))
def brief_audio_from_output(output_text: str, brief_length: int = 120) -> ResponseWrapper:
    # Trim output to a short briefing (you could also call a summarizer first)
    brief = output_text[:brief_length]
    audio_bytes = generate_speech(brief)
    return ResponseWrapper(output=audio_bytes, metadata={'provider': 'azure_speech', 'voice': 'en-US-JennyNeural'})

# Example usage (uncomment)
# if __name__ == '__main__':
#     result = brief_audio_from_output("This is a sample briefing about the latest AI breakthroughs.", brief_length=80)
#     with open('brief.mp3', 'wb') as f:
#         f.write(result.output)
