from google.cloud import speech
import io

def transcribe_audio(audio_bytes, language_code="en-US", sample_rate_hertz=16000):
    client = speech.SpeechClient()
    audio = speech.RecognitionAudio(content=audio_bytes)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.MP3, # Assuming MP3 from TTS synthesis
        sample_rate_hertz=sample_rate_hertz,
        language_code=language_code,
    )

    response = client.recognize(config=config, audio=audio)

    transcripts = []
    for result in response.results:
        transcripts.append(result.alternatives[0].transcript)
    
    return {"transcripts": transcripts}
