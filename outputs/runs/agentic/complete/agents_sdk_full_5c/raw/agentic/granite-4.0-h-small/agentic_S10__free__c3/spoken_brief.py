import os
from model_client import get_llm_client
from model_models import InferenceResponse

def generate_spoken_brief(summary_text: str, voice: str = "alloy") -> str:
    """Create a brief spoken narration from model output using a hosted TTS service.

    Args:
        summary_text: The text to be spoken.
        voice: Identifier for the voice model (default: "alloy").

    Returns:
        A string representing the URL or identifier of the generated audio file.
    """
    client = get_llm_client("tts")  # Use a generic client; real implementation would target a TTS API.
    payload = {
        "model": "tts",
        "voice": voice,
        "input": summary_text,
        "format": "mp3",
    }
    response = client.text_to_speech(payload)  # type: ignore
    # Assume response contains a field 'audio_url' with the hosted audio file link
    audio_url = response.audio_url  # type: ignore
    return audio_url
