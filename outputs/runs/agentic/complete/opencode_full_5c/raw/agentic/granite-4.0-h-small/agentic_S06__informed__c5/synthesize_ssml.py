import os
from elevenlabs import ElevenLabs

# Initialize ElevenLabs client
client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))


def synthesize_ssml(
    ssml: str, voice_id: str = "11ead5fc-4bcf-4e4e-8c38-49d03cefae29"
) -> bytes:
    """Synthesize SSML with voice and prosody controls via ElevenLabs.

    Args:
        ssml (str): SSML string describing speech.
        voice_id (str): ElevenLabs voice identifier (default default voice).

    Returns:
        bytes: Audio byte stream of the synthesized speech.
    """
    # ElevenLabs SDK expects plain text; wrap SSML for processing
    response = client.text_to_speech(ssml, voice_id=voice_id)
    return response.audio_content
