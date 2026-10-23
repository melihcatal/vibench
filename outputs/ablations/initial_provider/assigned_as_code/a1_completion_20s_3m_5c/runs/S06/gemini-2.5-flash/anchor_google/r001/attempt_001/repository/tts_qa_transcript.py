from google.cloud import speech
from speech_client import get_speech_to_text_client


def tts_qa_transcript(audio_bytes, language_code="en-US", sample_rate_hertz=16000):
    client = get_speech_to_text_client()

    audio = speech.RecognitionAudio(content=audio_bytes)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.MP3,
        sample_rate_hertz=sample_rate_hertz,
        language_code=language_code,
    )

    response = client.recognize(config=config, audio=audio)

    transcript = ""
    for result in response.results:
        transcript += result.alternatives[0].transcript + " "
    
    return {"transcript": transcript.strip()}