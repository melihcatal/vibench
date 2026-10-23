from google.cloud import speech
from speech_client import GoogleSpeechClient
from speech_models import TranscriptionInput, TranscriptionOutput

def tts_qa_transcript(input: TranscriptionInput) -> TranscriptionOutput:
    client = GoogleSpeechClient()

    audio = speech.RecognitionAudio(content=input.audio_content)

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.MP3 if input.audio_format == "mp3" else speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000, # Assuming common sample rate, adjust if necessary
        language_code=input.language,
    )

    response = client.recognize(config=config, audio=audio)

    transcript = ""
    for result in response.results:
        transcript += result.alternatives[0].transcript

    return TranscriptionOutput(transcript=transcript)
