import os
import google.cloud.texttospeech as tts

# Helper utilities are imported from local modules
from speech_client import get_texttospeech_client
from speech_models import normalize_text

def synthesize_text(text: str, voice_name: str, audio_format: str = "mp3") -> bytes:
    """Synthesize plain text to an audio byte stream using Google Cloud Text‑to‑Speech.

    Args:
        text (str): The plain text to convert.
        voice_name (str): Voice identifier (e.g., "en-US-Wavenet-D").
        audio_format (str): Desired audio encoding (mp3, wav, ogg_opus, etc.).
    
    Returns:
        bytes: The raw audio data.
    """
    client = get_texttospeech_client()
    text = normalize_text(text)

    # Build the request payload
    synthesis_input = tts.SynthesisInput(text=text)
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

    # Call the provider
    response = client.synthesize_speech(request)
    # Return raw audio bytes (as received from the API)
    return response.audio_content

# Example usage (uncomment to test)
# if __name__ == "__main__":
#     audio = synthesize_text("Hello world!", "en-US-Wavenet-D")
#     with open("output.mp3", "wb") as f:
#         f.write(audio)
