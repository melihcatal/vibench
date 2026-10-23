from google.cloud import speech

def transcribe_audio_for_qa(audio_content: bytes, language_code: str = "en-US", sample_rate_hertz: int = 24000) -> str:
    client = speech.SpeechClient()
    audio = speech.RecognitionAudio(content=audio_content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16, # Assuming LINEAR16 as a common output from TTS
        sample_rate_hertz=sample_rate_hertz,
        language_code=language_code,
    )

    response = client.recognize(config=config, audio=audio)
    transcript_parts = []
    for result in response.results:
        transcript_parts.append(result.alternatives[0].transcript)
    return " ".join(transcript_parts)
