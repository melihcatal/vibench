from google.cloud import speech_v1p1beta1 as speech
import os


def tts_qa_transcript(payload, config=None):
    config = config or {}
    client = speech.SpeechClient()

    audio_bytes = payload.get("audio_bytes")
    sample_rate_hertz = payload.get("sample_rate_hertz", 24000) # Default for Polly mp3
    language_code = payload.get("language_code", "en-US")

    if not audio_bytes:
        raise ValueError("Audio bytes not provided in payload.")

    audio = speech.RecognitionAudio(content=audio_bytes)
    speech_config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.MP3, # Assuming MP3 from Polly
        sample_rate_hertz=sample_rate_hertz,
        language_code=language_code,
    )

    response = client.recognize(config=speech_config, audio=audio)

    transcript = ""
    for result in response.results:
        transcript += result.alternatives[0].transcript + " "
    
    return {"transcript": transcript.strip()}
