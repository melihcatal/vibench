"""
Generate spoken previews of translated copy.
Uses Google Cloud Text-to-Speech API (texttospeech.googleapis.com)
to synthesize audio previews of translated text.
Provider: Google Cloud Text-to-Speech (texttospeech.googleapis.com)
Model: Google WaveNet and Standard TTS voices
"""

from typing import Optional, List, Dict, Any
import base64
import os
import tempfile

from google.cloud import texttospeech
from google.api_core import client_info as google_client_info

from translation_models import TranslationResponse


GOOGLE_TTS_ENDPOINT = "texttospeech.googleapis.com"
GOOGLE_TTS_WAVENET_MODEL = "google-wavenet"
GOOGLE_TTS_STANDARD_MODEL = "google-standard"


VOICE_CONFIG = {
    "en": {"language_code": "en-US", "name": "en-US-Wavenet-D", "ssml_gender": texttospeech.SsmlVoiceGender.NEUTRAL},
    "es": {"language_code": "es-ES", "name": "es-ES-Wavenet-B", "ssml_gender": texttospeech.SsmlVoiceGender.FEMALE},
    "fr": {"language_code": "fr-FR", "name": "fr-FR-Wavenet-A", "ssml_gender": texttospeech.SsmlVoiceGender.FEMALE},
    "de": {"language_code": "de-DE", "name": "de-DE-Wavenet-A", "ssml_gender": texttospeech.SsmlVoiceGender.FEMALE},
    "ja": {"language_code": "ja-JP", "name": "ja-JP-Wavenet-A", "ssml_gender": texttospeech.SsmlVoiceGender.FEMALE},
    "zh": {"language_code": "cmn-CN", "name": "cmn-CN-Wavenet-A", "ssml_gender": texttospeech.SsmlVoiceGender.FEMALE},
    "pt": {"language_code": "pt-BR", "name": "pt-BR-Wavenet-A", "ssml_gender": texttospeech.SsmlVoiceGender.FEMALE},
    "it": {"language_code": "it-IT", "name": "it-IT-Wavenet-A", "ssml_gender": texttospeech.SsmlVoiceGender.FEMALE},
    "ko": {"language_code": "ko-KR", "name": "ko-KR-Wavenet-A", "ssml_gender": texttospeech.SsmlVoiceGender.FEMALE},
    "ru": {"language_code": "ru-RU", "name": "ru-RU-Wavenet-A", "ssml_gender": texttospeech.SsmlVoiceGender.FEMALE},
}


def create_tts_client() -> texttospeech.TextToSpeechClient:
    """
    Create a Google Cloud Text-to-Speech API client.
    
    Uses google.cloud.texttospeech to connect to texttospeech.googleapis.com
    for audio synthesis.
    
    Returns:
        Configured google.cloud.texttospeech.TextToSpeechClient instance.
    """
    client_info = google_client_info.ClientInfo(
        user_agent="localized-audio-preview/1.0"
    )
    
    client = texttospeech.TextToSpeechClient(
        client_info=client_info,
    )
    
    return client


def synthesize_audio(
    text: str,
    language_code: str = "en-US",
    voice_name: Optional[str] = None,
    ssml_gender: Optional[texttospeech.SsmlVoiceGender] = None,
    speaking_rate: float = 1.0,
    pitch: float = 0.0,
    audio_encoding: texttospeech.AudioEncoding = texttospeech.AudioEncoding.MP3,
    client: Optional[texttospeech.TextToSpeechClient] = None,
) -> Dict[str, Any]:
    """
    Synthesize audio from text using Google Cloud Text-to-Speech.
    
    Uses the google.cloud.texttospeech client to generate audio via
    texttospeech.googleapis.com with WaveNet or Standard voices.
    
    Args:
        text: Text to synthesize.
        language_code: BCP-47 language code (e.g., 'en-US', 'es-ES').
        voice_name: Specific voice name (e.g., 'en-US-Wavenet-D').
        ssml_gender: Voice gender preference.
        speaking_rate: Speech rate multiplier (0.25 to 4.0).
        pitch: Pitch adjustment in semitones (-20.0 to 20.0).
        audio_encoding: Audio encoding format.
        client: TTS client instance. Created if None.
    
    Returns:
        Dict with audio data (base64), metadata, and config.
    """
    if client is None:
        client = create_tts_client()
    
    voice_config = {}
    if voice_name:
        voice_config["name"] = voice_name
    else:
        lang_prefix = language_code.split("-")[0].lower()
        if lang_prefix in VOICE_CONFIG:
            voice_config["name"] = VOICE_CONFIG[lang_prefix]["name"]
            voice_config["language_code"] = VOICE_CONFIG[lang_prefix]["language_code"]
        else:
            voice_config["language_code"] = language_code
    
    if ssml_gender is not None:
        voice_config["ssml_gender"] = ssml_gender
    elif "ssml_gender" not in voice_config:
        voice_config["ssml_gender"] = texttospeech.SsmlVoiceGender.NEUTRAL
    
    if "language_code" not in voice_config:
        voice_config["language_code"] = language_code
    
    synthesis_input = texttospeech.SynthesisInput(text=text)
    
    voice = texttospeech.VoiceSelectionParams(
        language_code=voice_config.get("language_code", language_code),
        name=voice_config.get("name", ""),
        ssml_gender=voice_config.get("ssml_gender", texttospeech.SsmlVoiceGender.NEUTRAL),
    )
    
    audio_config = texttospeech.AudioConfig(
        audio_encoding=audio_encoding,
        speaking_rate=speaking_rate,
        pitch=pitch,
    )
    
    try:
        response = client.synthesize_speech(
            input=synthesis_input,
            voice=voice,
            audio_config=audio_config,
        )
        
        audio_content = response.audio_content
        audio_base64 = base64.b64encode(audio_content).decode("utf-8")
        audio_size_bytes = len(audio_content)
        
        model_type = "wavenet" if "wavenet" in voice.name.lower() else "standard"
        
        return {
            "audio_base64": audio_base64,
            "audio_size_bytes": audio_size_bytes,
            "text_length": len(text),
            "language_code": language_code,
            "voice_name": voice.name,
            "model_type": model_type,
            "speaking_rate": speaking_rate,
            "pitch": pitch,
            "encoding": str(audio_encoding),
            "success": True,
        }
    
    except Exception as e:
        return {
            "audio_base64": "",
            "audio_size_bytes": 0,
            "text_length": len(text),
            "language_code": language_code,
            "voice_name": voice.name if voice else "",
            "model_type": "unknown",
            "error": str(e),
            "success": False,
        }


def generate_audio_previews(
    translation_response: TranslationResponse,
    target_language: Optional[str] = None,
    speaking_rate: float = 1.0,
    pitch: float = 0.0,
    max_segments: int = 10,
    client: Optional[texttospeech.TextToSpeechClient] = None,
) -> List[Dict[str, Any]]:
    """
    Generate spoken audio previews for translated text segments.
    
    Uses Google Cloud Text-to-Speech API (texttospeech.googleapis.com) via
    google.cloud.texttospeech to synthesize audio for each translated segment.
    Supports WaveNet voices for high-quality audio generation.
    
    Args:
        translation_response: TranslationResponse with translated segments.
        target_language: Target language code for voice selection.
        speaking_rate: Speech rate multiplier.
        pitch: Pitch adjustment in semitones.
        max_segments: Maximum number of segments to generate audio for.
        client: TTS client instance. Created if None.
    
    Returns:
        List of audio preview dicts with base64 audio and metadata.
    """
    if client is None:
        client = create_tts_client()
    
    if not translation_response.success or not translation_response.results:
        return []
    
    target_lang = target_language or translation_response.results[0].target_language
    
    if target_lang:
        voice_info = VOICE_CONFIG.get(target_lang.lower(), {})
        language_code = voice_info.get("language_code", f"{target_lang}-{target_lang.upper()}")
    else:
        language_code = "en-US"
    
    audio_previews = []
    segments_to_process = translation_response.results[:max_segments]
    
    for result in segments_to_process:
        if not result.translated_text or not result.translated_text.strip():
            continue
        
        preview_text = result.translated_text
        if len(preview_text) > 500:
            preview_text = preview_text[:497] + "..."
        
        audio_result = synthesize_audio(
            text=preview_text,
            language_code=language_code,
            speaking_rate=speaking_rate,
            pitch=pitch,
            client=client,
        )
        
        audio_result["source_text"] = result.original_text
        audio_result["target_text"] = result.translated_text
        audio_result["source_language"] = result.source_language
        audio_result["target_language"] = result.target_language
        
        audio_previews.append(audio_result)
    
    return audio_previews


def save_audio_to_file(
    audio_preview: Dict[str, Any],
    filepath: str,
) -> bool:
    """
    Save audio preview to a file.
    
    Args:
        audio_preview: Audio preview dict from synthesize_audio.
        filepath: Path to save the audio file.
    
    Returns:
        True if save was successful.
    """
    if not audio_preview.get("audio_base64"):
        return False
    
    audio_bytes = base64.b64decode(audio_preview["audio_base64"])
    
    with open(filepath, "wb") as f:
        f.write(audio_bytes)
    
    return True


def generate_preview_urls(
    audio_previews: List[Dict[str, Any]],
    output_dir: str = "audio_previews",
) -> List[Dict[str, str]]:
    """
    Save audio previews to files and return file paths.
    
    Args:
        audio_previews: List of audio preview dicts.
        output_dir: Directory to save audio files.
    
    Returns:
        List of dicts with segment info and file paths.
    """
    os.makedirs(output_dir, exist_ok=True)
    
    url_entries = []
    
    for idx, preview in enumerate(audio_previews):
        if not preview.get("success"):
            continue
        
        lang = preview.get("target_language", "unknown")
        filepath = os.path.join(output_dir, f"preview_{idx}_{lang}.mp3")
        
        if save_audio_to_file(preview, filepath):
            url_entries.append({
                "segment_index": idx,
                "language": lang,
                "source_text": preview.get("source_text", ""),
                "target_text": preview.get("target_text", ""),
                "file_path": filepath,
                "voice": preview.get("voice_name", ""),
            })
    
    return url_entries


if __name__ == "__main__":
    from translate_text import translate_text
    
    response = translate_text("Hello, welcome to our application", target_language="es")
    if response.success:
        previews = generate_audio_previews(response, target_language="es")
        print(f"Generated {len(previews)} audio preview(s)")
        if previews:
            print(f"Voice: {previews[0].get('voice_name')}")
            print(f"Audio size: {previews[0].get('audio_size_bytes')} bytes")
