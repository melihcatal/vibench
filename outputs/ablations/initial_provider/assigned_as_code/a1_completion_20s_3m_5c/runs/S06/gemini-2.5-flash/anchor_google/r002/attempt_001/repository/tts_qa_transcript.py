from google.cloud import speech_v1 as speech
from google.cloud.speech_v1 import enums

def tts_qa_transcript(audio_bytes: bytes, language_code: str = "en-US", sample_rate_hertz: int = 16000):
    client = speech.SpeechClient()

    audio = speech.RecognitionAudio(content=audio_bytes)
    config = speech.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.MP3, # Assuming MP3 for synthesized audio
        sample_rate_hertz=sample_rate_hertz,
        language_code=language_code,
    )

    response = client.recognize(config=config, audio=audio)

    transcripts = []
    for result in response.results:
        transcripts.append(result.alternatives[0].transcript)

    return {"transcripts": transcripts}
