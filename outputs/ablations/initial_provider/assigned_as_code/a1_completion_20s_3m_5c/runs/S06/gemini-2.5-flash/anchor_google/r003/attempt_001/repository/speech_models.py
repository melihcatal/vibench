from typing import Dict, Any

def create_synthesis_input(text: str = None, ssml: str = None) -> Dict[str, Any]:
    """Creates a dictionary for synthesis input."""
    if text:
        return {"text": text}
    elif ssml:
        return {"ssml": ssml}
    else:
        raise ValueError("Either 'text' or 'ssml' must be provided.")

def parse_synthesis_response(response) -> Dict[str, Any]:
    """Parses the Text-to-Speech synthesis response."""
    return {"audio_bytes": response.audio_content, "content_type": "audio/mpeg"}

def normalize_voice_selection_params(language_code: str, voice_name: str = None) -> Dict[str, Any]:
    """Normalizes voice selection parameters."""
    params = {"language_code": language_code}
    if voice_name: params["name"] = voice_name
    return params

def normalize_audio_config(audio_encoding: str = "MP3", speaking_rate: float = 1.0, pitch: float = 0.0) -> Dict[str, Any]:
    """Normalizes audio configuration parameters."""
    return {"audio_encoding": audio_encoding, "speaking_rate": speaking_rate, "pitch": pitch}
