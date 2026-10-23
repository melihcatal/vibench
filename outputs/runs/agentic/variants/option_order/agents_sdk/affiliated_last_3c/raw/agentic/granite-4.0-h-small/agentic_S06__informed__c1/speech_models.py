import google.cloud.texttospeech as tts
from typing import List, Dict

def normalize_text(text: str) -> str:
    """Sanitize plain text for TTS.

    Strips null characters and limits length.
    """
    # Strip null bytes and trim to a safe length
    text = text.replace("\0", "")
    return text[:4000]  # TTS APIs often have payload limits

def normalize_ssml(ssml: str) -> str:
    """Sanitize SSML before synthesis.

    Ensures a top‑level <speak> tag and limits size.
    """
    if not ssml.strip().startswith("<speak"):
        ssml = f"<speak>{ssml}</speak>"
    return ssml[:5000]

def voice_to_dict(voice: tts.Voice) -> Dict[str, str]:
    """Convert a TextToSpeechClient.Voice protobuf to a simple dict.
    """
    return {
        "name": voice.name,
        "language_codes": voice.language_codes,
        "gender": voice.ssml_gender.name,
        "natural_sample_rate_Hz": voice.natural_sample_rate_hertz,
    }

# Example usage (uncomment to test)
# if __name__ == "__main__":
#     client = get_texttospeech_client()  # defined in speech_client.py
#     voices = client.list_voices().voices
#     for v in voices:
#         print(voice_to_dict(v))
