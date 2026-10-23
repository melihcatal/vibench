from google.cloud import speech
from google.cloud.speech import RecognitionConfig, RecognitionAudio
import os

def transcribe_qa_sample(audio_bytes, sample_rate_hertz, language_code, project_id=None):
    if not project_id:
        project_id = os.environ.get('GOOGLE_CLOUD_PROJECT')

    client = speech.SpeechClient(project=project_id)

    audio = RecognitionAudio(content=audio_bytes)
    config = RecognitionConfig(
        encoding=RecognitionConfig.AudioEncoding.MP3,
        sample_rate_hertz=sample_rate_hertz,
        language_code=language_code,
    )

    response = client.recognize(config=config, audio=audio)

    transcripts = []
    for result in response.results:
        transcripts.append(result.alternatives[0].transcript)
    
    return {"transcripts": transcripts}