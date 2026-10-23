# synthesize_ssml.py
# [SAME-SCENARIO] Synthesizes SSML with voice and prosody controls using Google Cloud Text-to-Speech.

from google.cloud import texttospeech
from speech_client import get_texttospeech_client

def synthesize_ssml(ssml: str, voice_name: str = None, speaking_rate: float = 1.0, pitch: float = 0.0, volume_gain_db: float = 0.0) -> bytes:
    """Synthesize SSML to audio bytes.

    Args:
        ssml: SSML string to synthesize.
        voice_name: Optional specific voice name (e.g., 'en-US-Wavenet-D').
        speaking_rate: Multiplier for default speaking rate.
        pitch: Pitch adjustment in semitones.
        volume_gain_db: Volume adjustment in decibels.

    Returns:
        Raw audio bytes (default format: MP3).
    """
    client = get_texttospeech_client()
    # Build voice selection (default fallback if voice_name not provided)
    voice = texttospeech.VoiceSelectionParams(name=voice_name) if voice_name else texttospeech.VoiceSelectionParams(language_code='en-US')
    # Prosody adjustments via SSML tags
    prosody_attrs = {
        'rate': f'{speaking_rate}x' if speaking_rate != 1.0 else '',
        'pitch': f'{pitch}st' if pitch != 0.0 else '',
        'volume': f'{volume_gain_db}dB' if volume_gain_db != 0.0 else ''
    }
    # Wrap SSML with explicit prosody tags if any adjustment is present
    wrapped_ssml = ssml
    if any(prosody_attrs.values()):
        tag_attrs = ' '.join(f'{k}="{v}"' for k, v in prosody_attrs.items() if v)
        wrapped_ssml = f'<speak><prosody {tag_attrs}>{ssml}</prosody></speak>' if tag_attrs else f'<speak>{ssml}</speak>'
    # Audio configuration (MP3)
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
    # Build request
    synthesis_input = texttospeech.SynthesisInput(ssml=wrapped_ssml)
    request = texttospeech.SynthesizeSpeechRequest(input=synthesis_input, voice=voice, audio_config=audio_config)
    # Perform synthesis
    response = client.synthesize_speech(request=request)
    return response.audio_content
