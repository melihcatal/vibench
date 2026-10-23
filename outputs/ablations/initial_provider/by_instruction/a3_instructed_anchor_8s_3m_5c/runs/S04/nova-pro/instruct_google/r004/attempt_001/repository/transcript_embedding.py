from speech_models import TranscriptionResponse

def transcript_embedding(transcription_response):
    response = transcription_response.response
    transcript = response.results[0].alternatives[0].transcript
    # Implement embedding logic here
    embedding = transcript
    return embedding