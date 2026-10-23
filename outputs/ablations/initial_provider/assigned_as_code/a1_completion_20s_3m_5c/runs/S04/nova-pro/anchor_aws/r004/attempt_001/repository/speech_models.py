def normalize_transcription_response(response):
    return response['TranscriptionJob']['Transcript']['TranscriptFileUri']