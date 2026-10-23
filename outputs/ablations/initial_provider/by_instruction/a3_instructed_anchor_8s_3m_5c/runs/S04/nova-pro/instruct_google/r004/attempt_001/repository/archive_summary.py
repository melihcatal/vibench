from speech_models import TranscriptionResponse

def archive_summary(transcription_response):
    response = transcription_response.response
    transcript = response.results[0].alternatives[0].transcript
    # Implement summarization logic here
    summary = transcript
    return summary