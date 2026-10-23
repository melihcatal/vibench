import os
from speech_client import get_tts_client
from speech_models import normalize_text

def synthesize_ssml(ssml: str, voice_id: str = None) -> bytes:
    """Synthesize SSML (with prosody, voice selection) to an audio byte stream.

    Args:
        ssml: SSML string containing <speak>...</speak>.
        voice_id: Optional voice identifier (e.g., 'en-US-JennyNeural').

    Returns:
        Raw audio bytes (ogg/opus).
    """
    client = get_tts_client()
    # Azure Speech expects raw SSML without the outer <speak> tag
    plain_ssml = ssml.replace("<speak>", "").replace("</speak>", "")
    response = client.synthesize_speech(
        speech_config={"VoiceName": voice_id},
        audio_config={"Format": "OggOpus"},
        text=plain_ssml,
    )
    return response.audio_data

if __name__ == "__main__":
    ssml_example = "<speak>Hello, <prosody rate=\"slow\">world!</prosody></speak>"
    audio = synthesize_ssml(ssml_example, voice_id="en-US-JennyNeural")
    print(f"SSML audio size: {len(audio)} bytes")
