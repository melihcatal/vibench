import os
from typing import Dict
import assemblyai as aai


class TTSQATranscriber:
    """Transcribes synthesized QA samples to verify spoken output using AssemblyAI."""

    def __init__(self):
        aai.settings.api_key = os.getenv("ASSEMBLYAI_API_KEY")

    def transcribe_audio(self, audio_url: str) -> Dict:
        """
        Transcribes audio from a URL to verify spoken output.

        Args:
            audio_url: The URL of the audio file to transcribe.

        Returns:
            Dict: The transcription results.

        Raises:
            Exception: If the transcription fails.
        """
        transcriber = aai.Transcriber()
        transcript = transcriber.transcribe(audio_url)
        if transcript.status == aai.TranscriptStatus.error:
            raise Exception(transcript.error)
        return {
            "text": transcript.text,
            "confidence": transcript.confidence,
            "words": [
                {"text": word.text, "confidence": word.confidence}
                for word in transcript.words
            ],
        }
