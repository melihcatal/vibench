from typing import Dict, Any, List

def create_synthesis_request(text: str, voice_params: Dict[str, str], audio_format: str) -> Dict[str, Any]:
    return {
        "text": text,
        "voice_params": voice_params,
        "audio_format": audio_format
    }

def create_ssml_synthesis_request(ssml_text: str, voice_id: str, output_format: str) -> Dict[str, Any]:
    return {
        "ssml_text": ssml_text,
        "voice_id": voice_id,
        "output_format": output_format
    }

def create_voice_selection_params(language_code: str, voice_name: str = None, gender: str = None) -> Dict[str, str]:
    params = {"language_code": language_code}
    if voice_name: 
        params["name"] = voice_name
    if gender: 
        params["gender"] = gender
    return params

def parse_voice_list_response(response_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    # Example of a simple parser/normalizer for voice data
    normalized_voices = []
    for voice in response_data:
        normalized_voices.append({
            "name": voice.get("FriendlyName", voice.get("DisplayName")),
            "locale": voice.get("Locale"),
            "gender": voice.get("Gender"),
            "short_name": voice.get("ShortName")
        })
    return normalized_voices
