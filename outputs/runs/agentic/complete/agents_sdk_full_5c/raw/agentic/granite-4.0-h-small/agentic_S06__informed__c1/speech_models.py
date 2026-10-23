import json
from typing import Dict, Any

# Constants for supported services (mirrored from TTS_SERVICES in speech_client.py)
MODEL_IDS = {
    'google-cloud-texttospeech': 'en-US-Wavenet-D',
    'ibm-watson': 'en-US_MichaelV3Voice',
    'azure-cognitiveservices-speech': 'en-US-AriaNeural',
    'dashscope': 'cosyvoice-eng',
    'elevenlabs': 'elevenlabs:1',
    'boto3': 'Joanna',
}

# Normalization helpers (placeholder functions; can be expanded)
def normalize_request(request: Dict[str, Any]) -> Dict[str, Any]:
    """Convert a generic request dict into provider-specific format.","""
    return request  # stub for illustration

def normalize_response(response: Dict[str, Any]) -> Dict[str, Any]:
    """Convert provider-specific response into a generic dict.","""
    return response  # stub for illustration

if __name__ == '__main__':
    print('Sample normalization utilities loaded.')
