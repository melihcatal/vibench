from speech_models import TranscriptionResponse

def moderate_transcript(transcription_response):
    response = transcription_response.response
    transcript = response.results[0].alternatives[0].transcript
    # Implement moderation logic here
    moderated_transcript = transcript
    return moderated_transcript