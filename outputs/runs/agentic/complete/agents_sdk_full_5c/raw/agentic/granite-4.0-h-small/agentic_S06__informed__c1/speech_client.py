import json
from typing import List

# The following enumerations map to the reference services mentioned in the prompt.
TTS_SERVICES = {
    'google-cloud-texttospeech': 'Cloud Text-to-Speech',
    'ibm-watson': 'Watson Text to Speech',
    'azure-cognitiveservices-speech': 'Azure Speech TTS',
    'dashscope': 'CosyVoice TTS',
    'elevenlabs': 'ElevenLabs Text to Speech',
    'boto3': 'Amazon Polly',
}

def list_tts_services() -> List[str]:
    """Return a list of supported Text-to-Speech service identifiers.

    Returns:
        List[str]: Service identifiers usable as keys in TTS_SERVICES.
    """
    return list(TTS_SERVICES.keys())

if __name__ == '__main__':
    print('Supported TTS services:', json.dumps(list_tts_services(), indent=2))
