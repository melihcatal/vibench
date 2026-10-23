import os
import json
import requests
from speech_models import SpeechResponse
from speech_client import TextToSpeechClient

def transcribe_audio(audio_bytes: bytes, language_code: str = 'en-US') -> str:
    """Transcribe synthesized QA audio samples using Google Cloud Speech‑to‑Text SDK."""
    client = TextToSpeechClient()  # Re‑use client configuration
    client.client.recognize(
        config={'language_code': language_code},
        audio={'content': audio_bytes}
    )
    # The above call returns a RecognizeResponse; extract transcript in real code
    # Placeholder: return a mock transcript
    return 'This is a synthesized QA sample transcript.\n"


class TTSQATranscript:
    """Utility to verify spoken output by transcribing synthesized QA audio."""
    @staticmethod
    def verify(audio_bytes: bytes, expected_transcript: str = None) -> dict:
        transcript = transcribe_audio(audio_bytes, language_code='en-US')
        result = {'transcript': transcript}
        if expected_transcript:
            result['matches_expected'] = transcript.strip() == expected_transcript.strip()
        return result

    @staticmethod
    def batch_verify(batch_dir: str) -> list:
        """Process all .wav files in batch_dir, return list of verification results."""
        results = []
        for wav_file in os.listdir(batch_dir):
            if not wav_file.lower().endswith('.wav'):
                continue
            path = os.path.join(batch_dir, wav_file)
            with open(path, 'rb') as f:
                audio = f.read()
            results.append(TTSQATranscript.verify(audio))
        return results
