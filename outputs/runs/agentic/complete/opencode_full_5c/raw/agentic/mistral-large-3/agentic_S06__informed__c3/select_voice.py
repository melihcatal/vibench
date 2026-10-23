from typing import List, Dict, Optional
import os
from google.cloud import texttospeech_v1 as texttospeech
from google.api_core.exceptions import GoogleAPICallError


class VoiceSelector:
    """Lists or selects a voice for a target locale using Google Cloud Text-to-Speech."""

    def __init__(self):
        self.client = texttospeech.TextToSpeechClient()

    def list_voices(self, language_code: Optional[str] = None) -> List[Dict[str, str]]:
        """
        Lists available voices for a target locale.

        Args:
            language_code: The language code to filter voices (e.g., "en-US").

        Returns:
            List[Dict[str, str]]: A list of available voices with their names and languages.

        Raises:
            GoogleAPICallError: If the request fails.
        """
        response = self.client.list_voices(language_code=language_code)
        voices = []
        for voice in response.voices:
            voices.append(
                {
                    "name": voice.name,
                    "language_codes": list(voice.language_codes),
                    "ssml_gender": texttospeech.SsmlVoiceGender(voice.ssml_gender).name,
                }
            )
        return voices

    def select_voice(
        self, language_code: str, voice_name: Optional[str] = None
    ) -> Dict[str, str]:
        """
        Selects a voice for a target locale.

        Args:
            language_code: The language code of the voice (e.g., "en-US").
            voice_name: The name of the voice to select (e.g., "en-US-Wavenet-D").

        Returns:
            Dict[str, str]: The selected voice details.

        Raises:
            GoogleAPICallError: If the request fails.
        """
        voices = self.list_voices(language_code=language_code)
        if voice_name:
            for voice in voices:
                if voice["name"] == voice_name:
                    return voice
            raise ValueError(
                f"Voice {voice_name} not found for language {language_code}"
            )
        return voices[0] if voices else {}
