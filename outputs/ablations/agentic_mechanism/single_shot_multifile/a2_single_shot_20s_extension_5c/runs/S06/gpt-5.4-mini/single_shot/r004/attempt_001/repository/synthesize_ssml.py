from __future__ import annotations

from typing import Optional

from speech_client import build_client, get_text_to_speech_provider
from speech_models import SynthesisRequest, normalize_voice_name


def synthesize_ssml(ssml: str, voice: Optional[str] = None, language_code: Optional[str] = None, rate: Optional[str] = None, pitch: Optional[str] = None) -> bytes:
    provider = get_text_to_speech_provider()
    client = build_client()
    request = SynthesisRequest(text=ssml, language_code=language_code, voice=normalize_voice_name(voice), rate=rate, pitch=pitch, is_ssml=True)
    if provider == "google":
        from google.cloud import texttospeech

        synthesis_input = texttospeech.SynthesisInput(ssml=request.text)
        voice_params = texttospeech.VoiceSelectionParams(language_code=request.language_code or "en-US", name=request.voice or "en-US-Standard-C")
        speaking_rate = float(request.rate) if request.rate else 1.0
        pitch_value = float(request.pitch) if request.pitch else 0.0
        audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3, speaking_rate=speaking_rate, pitch=pitch_value)
        response = client.synthesize_speech(input=synthesis_input, voice=voice_params, audio_config=audio_config)
        return bytes(response.audio_content)
    if provider == "azure":
        import azure.cognitiveservices.speech as speechsdk

        speech_config = client
        result = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=None).speak_ssml_async(request.text).get()
        return bytes(result.audio_data)
    if provider == "aws":
        response = client.synthesize_speech(Text=request.text, TextType="ssml", VoiceId=request.voice or "Joanna", OutputFormat="mp3", LanguageCode=request.language_code or "en-US")
        return response["AudioStream"].read()
    if provider == "openai":
        import requests

        api_key = client
        response = requests.post("https://api.openai.com/v1/audio/speech", headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}, json={"model": "gpt-4o-mini-tts", "input": request.text, "voice": request.voice or "alloy", "format": "mp3"}, timeout=60)
        response.raise_for_status()
        return response.content
    if provider == "elevenlabs":
        import requests

        api_key = client
        voice_id = request.voice or "21m00Tcm4TlvDq8ikWAM"
        response = requests.post(f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}", headers={"xi-api-key": api_key, "accept": "audio/mpeg", "content-type": "application/json"}, json={"text": request.text, "model_id": "eleven_multilingual_v2", "voice_settings": {"stability": 0.5, "similarity_boost": 0.75}}, timeout=60)
        response.raise_for_status()
        return response.content
    raise RuntimeError(f"Unsupported TTS provider: {provider}")
