from google.cloud import speech
from typing import Optional

def tts_qa_transcript(
    audio_content: bytes,
    language_code: str = "en-US",
    sample_rate_hertz: Optional[int] = 24000
) -> str:
    """
    Transcribe synthesized QA samples using Google Cloud Speech-to-Text.
    """
    client = speech.SpeechClient()
    audio = speech.RecognitionAudio(content=audio_content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.MP3,
        sample_rate_hertz=sample_rate_hertz,
        language_code=language_code,
        enable_automatic_punctuation=True,
        enable_word_time_offsets=False
    )
    response = client.recognize(config=config, audio=audio)
    if not response.results:
        return ""
    transcripts = [
        result.alternatives[0].transcript
        for result in response.results
    ]
    return " ".join(transcripts)
