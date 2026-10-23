from google.cloud import speech_v1p1beta1 as speech
from typing import List, Dict

def transcribe_synthesized_audio(audio_content: bytes, language_code: str = "en-US") -> Dict[str, List[str]]:
    client = speech.SpeechClient()
    audio = speech.RecognitionAudio(content=audio_content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.MP3,
        sample_rate_hertz=24000,
        language_code=language_code,
        enable_automatic_punctuation=True
    )
    response = client.recognize(config=config, audio=audio)
    transcripts = [
        result.alternatives[0].transcript for result in response.results
    ]
    return {"transcripts": transcripts}