import os
import google.cloud.texttospeech as tts

# Helper utilities are imported from local modules
from speech_client import get_texttospeech_client
from speech_models import normalize_ssml

def synthesize_ssml(ssml: str, voice_name: str, audio_format: str = "mp3") -> bytes:
    """Synthesize SSML marked‑up text to an audio byte stream using Google Cloud Text‑to‑Speech.

    Args:
        ssml (str): SSML string (e.g., '<speak>Hello <break time="500ms"/> world!</speak>').
        voice_name (str): Voice identifier (e.g., "en-US-Wavenet-D").
        audio_format (str): Desired audio encoding (mp3, wav, ogg_opus, etc.).
    
    Returns:
        bytes: The raw audio data.
    """
    client = get_texttospeech_client()
    ssml = normalize_ssml(ssml)

    synthesis_input = tts.SynthesisInput(ssml=ssml)
    voice = tts.VoiceSelectionParams(
        language_code=voice_name.split('-')[0],
        name=voice_name
    )
    audio_config = tts.AudioConfig(
        audio_encoding=getattr(tts.AudioEncoding, audio_format.upper()),
    )

    request = tts.SynthesizeSpeechRequest(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config,
    )

    response = client.synthesize_speech(request)
    return response.audio_content

# Example usage (uncomment to test)
# if __name__ == "__main__":
#     audio = synthesize_ssml('<speak>Hello <break time="500ms"/> world!</speak>', "en-US-Wavenet-D")
#     with open("output_ssml.mp3", "wb") as f:
#         f.write(audio)
