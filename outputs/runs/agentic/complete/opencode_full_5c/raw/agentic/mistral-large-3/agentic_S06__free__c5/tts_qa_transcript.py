from google.cloud import speech_v1p1beta1 as speech
from typing import List, Dict


def transcribe_audio(audio_content: bytes, language_code: str = "en-US") -> str:
    """
    Transcribes synthesized QA samples to verify spoken output using Google Cloud Speech-to-Text.
    """
    client = speech.SpeechClient()

    audio = speech.RecognitionAudio(content=audio_content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.MP3,
        sample_rate_hertz=24000,
        language_code=language_code,
        enable_automatic_punctuation=True,
    )

    response = client.recognize(config=config, audio=audio)

    transcript = ""
    for result in response.results:
        transcript += result.alternatives[0].transcript

    return transcript


def batch_transcribe_audio(
    audio_contents: List[bytes], language_code: str = "en-US"
) -> List[str]:
    """
    Transcribes a batch of synthesized QA samples to verify spoken output.
    """
    client = speech.SpeechClient()

    transcripts = []
    for audio_content in audio_contents:
        audio = speech.RecognitionAudio(content=audio_content)
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.MP3,
            sample_rate_hertz=24000,
            language_code=language_code,
            enable_automatic_punctuation=True,
        )

        response = client.recognize(config=config, audio=audio)

        transcript = ""
        for result in response.results:
            transcript += result.alternatives[0].transcript

        transcripts.append(transcript)

    return transcripts
