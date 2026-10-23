"""
speech_client.py - Provide local configuration and client helper utilities for Text-to-Speech.

Manages Google Cloud Text-to-Speech client initialization, authentication,
and convenience wrappers for common TTS operations. Uses the google-cloud-texttospeech SDK.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Dict, List, Optional

from google.cloud import texttospeech
from google.cloud.texttospeech_v1.types import (
    AudioConfig,
    AudioEncoding,
    SsmlVoiceGender,
    SynthesisInput,
    VoiceSelectionParams,
)

from speech_models import (
    AudioEncodingEnum,
    SSMLSynthesisRequest,
    SynthesisRequest,
    SynthesisResponse,
    VoiceFilter,
    VoiceInfo,
    VoiceListResponse,
)


DEFAULT_SAMPLE_RATE = 24000
DEFAULT_ENCODING = AudioEncoding.MP3


def _map_encoding(encoding: AudioEncodingEnum) -> AudioEncoding:
    """Map AudioEncodingEnum to google.cloud.texttospeech_v1.AudioEncoding."""
    encoding_map = {
        AudioEncodingEnum.LINEAR16: AudioEncoding.LINEAR16,
        AudioEncodingEnum.MP3: AudioEncoding.MP3,
        AudioEncodingEnum.OGG_OPUS: AudioEncoding.OGG_OPUS,
        AudioEncodingEnum.MULAW: AudioEncoding.MULAW,
    }
    return encoding_map.get(encoding, AudioEncoding.MP3)


class SpeechClientHelper:
    """
    Helper class that wraps google.cloud.texttospeech.TextToSpeechClient
    with normalized request/response handling and local configuration.
    """

    def __init__(
        self,
        project_id: Optional[str] = None,
        credentials_path: Optional[str] = None,
        api_endpoint: Optional[str] = None,
    ):
        """
        Initialize the Google Cloud TTS client helper.

        Args:
            project_id: Google Cloud project ID. Falls back to GOOGLE_CLOUD_PROJECT env var.
            credentials_path: Path to service account JSON. Falls back to GOOGLE_APPLICATION_CREDENTIALS.
            api_endpoint: Optional custom API endpoint.
        """
        self.project_id = project_id or os.environ.get("GOOGLE_CLOUD_PROJECT", "")
        creds_path = credentials_path or os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")

        client_options: Dict[str, Any] = {}
        if api_endpoint:
            client_options["api_endpoint"] = api_endpoint

        if creds_path:
            from google.oauth2 import service_account

            credentials = service_account.Credentials.from_service_account_file(creds_path)
            self.client = texttospeech.TextToSpeechClient(
                client_options=client_options,
                credentials=credentials,
            )
        else:
            self.client = texttospeech.TextToSpeechClient(client_options=client_options)

    def synthesize_text(self, request: SynthesisRequest) -> SynthesisResponse:
        """
        Synthesize plain text to audio using Google Cloud Text-to-Speech.

        Args:
            request: SynthesisRequest with text and voice parameters.

        Returns:
            SynthesisResponse containing synthesized audio bytes.
        """
        input_text = SynthesisInput(text=request.text)

        voice_params = VoiceSelectionParams(
            language_code=request.language_code,
        )
        if request.voice_name:
            voice_params.name = request.voice_name
        if request.ssml_gender:
            gender_map = {
                "MALE": SsmlVoiceGender.MALE,
                "FEMALE": SsmlVoiceGender.FEMALE,
                "NEUTRAL": SsmlVoiceGender.NEUTRAL,
            }
            voice_params.ssml_gender = gender_map.get(request.ssml_gender, SsmlVoiceGender.NEUTRAL)

        audio_config = AudioConfig(
            audio_encoding=_map_encoding(request.encoding),
            speaking_rate=request.speaking_rate,
            pitch=request.pitch,
            volume_gain_db=request.volume_gain_db,
            sample_rate_hertz=request.sample_rate_hertz,
        )

        response = self.client.synthesize_speech(
            input=input_text,
            voice=voice_params,
            audio_config=audio_config,
        )

        return SynthesisResponse(
            audio_content=response.audio_content,
            encoding=request.encoding,
            sample_rate_hertz=request.sample_rate_hertz,
            audio_length_bytes=len(response.audio_content),
        )

    def synthesize_ssml(self, request: SSMLSynthesisRequest) -> SynthesisResponse:
        """
        Synthesize SSML markup to audio using Google Cloud Text-to-Speech.

        Args:
            request: SSMLSynthesisRequest with SSML and voice parameters.

        Returns:
            SynthesisResponse containing synthesized audio bytes.
        """
        input_ssml = SynthesisInput(ssml=request.ssml)

        voice_params = VoiceSelectionParams(
            language_code=request.language_code,
        )
        if request.voice_name:
            voice_params.name = request.voice_name
        if request.ssml_gender:
            gender_map = {
                "MALE": SsmlVoiceGender.MALE,
                "FEMALE": SsmlVoiceGender.FEMALE,
                "NEUTRAL": SsmlVoiceGender.NEUTRAL,
            }
            voice_params.ssml_gender = gender_map.get(request.ssml_gender, SsmlVoiceGender.NEUTRAL)

        audio_config = AudioConfig(
            audio_encoding=_map_encoding(request.encoding),
            speaking_rate=request.speaking_rate,
            pitch=request.pitch,
            volume_gain_db=request.volume_gain_db,
            sample_rate_hertz=request.sample_rate_hertz,
        )

        response = self.client.synthesize_speech(
            input=input_ssml,
            voice=voice_params,
            audio_config=audio_config,
        )

        return SynthesisResponse(
            audio_content=response.audio_content,
            encoding=request.encoding,
            sample_rate_hertz=request.sample_rate_hertz,
            audio_length_bytes=len(response.audio_content),
        )

    def list_voices(self, filter_params: VoiceFilter) -> VoiceListResponse:
        """
        List available voices from Google Cloud Text-to-Speech matching filter criteria.

        Args:
            filter_params: VoiceFilter with language and gender constraints.

        Returns:
            VoiceListResponse containing matching VoiceInfo objects.
        """
        language_codes = [filter_params.language_code]
        response = self.client.list_voices(language_codes=language_codes)

        voices: List[VoiceInfo] = []
        for v in response.voices:
            if filter_params.ssml_gender:
                gender_map = {
                    "MALE": SsmlVoiceGender.MALE,
                    "FEMALE": SsmlVoiceGender.FEMALE,
                    "NEUTRAL": SsmlVoiceGender.NEUTRAL,
                }
                target_gender = gender_map.get(filter_params.ssml_gender)
                if target_gender and v.ssml_gender != target_gender:
                    continue

            voices.append(
                VoiceInfo(
                    name=v.name,
                    language_code=v.language_codes[0] if v.language_codes else filter_params.language_code,
                    ssml_gender=SsmlVoiceGender(v.ssml_gender).name if v.ssml_gender else "NEUTRAL",
                    natural_sample_rate_hertz=v.natural_sample_rate_hertz,
                    supported_models=[str(m) for m in v.supported_model_types] if v.supported_model_types else [],
                )
            )

        return VoiceListResponse(voices=voices)

    def select_voice(self, filter_params: VoiceFilter) -> Optional[VoiceInfo]:
        """
        Select the best matching voice for given criteria.
        Prefers Neural2 voices, then WaveNet, then Standard.

        Args:
            filter_params: VoiceFilter with selection criteria.

        Returns:
            VoiceInfo for the best match or None.
        """
        voice_list = self.list_voices(filter_params)
        if not voice_list.voices:
            return None

        model_priority = {
            "NEURAL2": 0,
            "STUDIO": 1,
            "WAVENET": 2,
            "STANDARD": 3,
        }

        best_voice = None
        best_priority = float("inf")

        for voice in voice_list.voices:
            priority = best_priority
            for model in voice.supported_models:
                model_upper = model.upper().replace("MODEL_TYPE_", "")
                if model_upper in model_priority:
                    priority = min(priority, model_priority[model_upper])

            if priority < best_priority:
                best_priority = priority
                best_voice = voice

        return best_voice or voice_list.voices[0]
