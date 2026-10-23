from speech_client import get_transcribe_client

def normalize_transcription_response(response):
    return response['TranscriptionJob']['Transcript']['TranscriptFileUri']

def normalize_translate_response(response):
    return response['TranslatedText']

def normalize_moderation_response(response):
    return response['ModerationLabels']

def normalize_summarization_response(response):
    return response['Summary']

def normalize_embedding_response(response):
    return response['Body'].read().decode('utf-8')