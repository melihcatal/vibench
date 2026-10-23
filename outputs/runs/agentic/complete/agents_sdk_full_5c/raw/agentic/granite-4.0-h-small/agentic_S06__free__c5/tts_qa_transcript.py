# tts_qa_transcript.py
# [LATER-STEP] Transcribe synthesized QA samples to verify spoken output using Google Cloud Speech-to-Text.

from google.cloud import speech_v1p1beta1 as speech
from speech_client import get_texttospeech_client  # reuse ADC handling (not used directly here)

def transcribe_audio(audio_bytes: bytes, language_code: str = 'en-US') -> str:
    """Transcribe an audio byte stream to text.

    Args:
        audio_bytes: Raw audio data (e.g., MP3 from TTS synthesis).
        language_code: BCP-47 language tag for transcribing.

    Returns:
        The first alternative transcription result, or an empty string on failure.
    """
    client = speech.SpeechClient()  # ADC credentials
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.MP3,
        language_code=language_code,
    )
    audio = speech.RecognitionAudio(content=audio_bytes)
    response = client.recognize(config=config, audio=audio)
    if response.results:
        return response.results[0].alternatives[0].transcript
    return ''
