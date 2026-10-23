from __future__ import annotations

import base64
from typing import Optional

from speech_client import build_client, get_text_to_speech_provider
from speech_models import SynthesisRequest, normalize_voice_name


def synthesize_text(text: str, voice: Optional[str] = None, language_code: Optional[str] = None) -> bytes:
    provider = get_text_to_speech_provider()
    client = build_client()
    request = SynthesisRequest(text=text, language_code=language_code, voice=normalize_voice_name(voice))
    if provider == "google":
        from google.cloud import texttospeech

        synthesis_input = texttospeech.SynthesisInput(text=request.text)
        voice_params = texttospeech.VoiceSelectionParams(language_code=request.language_code or "en-US", name=request.voice or "en-US-Standard-C")
        audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
        response = client.synthesize_speech(input=synthesis_input, voice=voice_params, audio_config=audio_config)
        return bytes(response.audio_content)
    if provider == "azure":
        import azure.cognitiveservices.speech as speechsdk

        speech_config = client
        ssml = f'<speak version="1.0" xml:lang="{request.language_code or "en-US"}"><voice name="{request.voice or "en-US-JennyNeural"}">{request.text}</voice></speak>'
        result = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=None).speak_ssml_async(ssml).get()
        return bytes(result.audio_data)
    if provider == "aws":
        response = client.synthesize_speech(Text=request.text, VoiceId=request.voice or "Joanna", OutputFormat="mp3", LanguageCode=request.language_code or "en-US")
        return response["AudioStream"].read()
    if provider == "openai":
        import requests

        api_key = client
        payload = {"model": "gpt-4o-mini-tts", "input": request.text, "voice": request.voice or "alloy", "format": "mp3"}
        response = requests.post("https://api.openai.com/v1/audio/speech", headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}, json=payload, timeout=60)
        response.raise_for_status()
        return response.content
    if provider == "elevenlabs":
        import requests

        api_key = client
        voice_id = request.voice or "21m00Tcm4TlvDq8ikWAM"
        response = requests.post(f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}", headers={"xi-api-key": api_key, "accept": "audio/mpeg", "content-type": "application/json"}, json={"text": request.text, "model_id": "eleven_multilingual_v2"}, timeout=60)
        response.raise_for_status()
        return response.content
    raise RuntimeError(f"Unsupported TTS provider: {provider}")
