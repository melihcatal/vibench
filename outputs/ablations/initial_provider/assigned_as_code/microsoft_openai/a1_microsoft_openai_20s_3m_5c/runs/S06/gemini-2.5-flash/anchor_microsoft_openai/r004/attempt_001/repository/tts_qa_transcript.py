from google.cloud import speech_v1p1beta1 as speech
import io

def transcribe_audio(audio_bytes: bytes, sample_rate_hertz: int, language_code: str = "en-US") -> dict:
    client = speech.SpeechClient()
    
    audio = speech.RecognitionAudio(content=audio_bytes)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.MP3,  # Assuming MP3 output from TTS
        sample_rate_hertz=sample_rate_hertz,
        language_code=language_code,
    )

    response = client.recognize(config=config, audio=audio)

    transcripts = []
    for result in response.results:
        transcripts.append(result.alternatives[0].transcript)

    return {"transcripts": transcripts, "full_response": response}
