
# [HELPER] speech_models.py
import os
import json

# Provider-specific configuration for Amazon Transcribe Streaming
# This module holds request/response models and normalization utilities.

# Supported language codes (Amazon Transcribe)
LANGUAGE_CODES = {
    'en-US': 'English (US)',
    'es-ES': 'Spanish (Spain)',
    'fr-FR': 'French (France)',
    'de-DE': 'German (Germany)',
    # Add more as needed
}

# Request payload structure for start_stream_transcription
STREAM_REQUEST_KEYS = [
    'LanguageCode',
    'MediaSampleRateHertz',
    'MediaType',
    'VocabularyName',  # optional
]

# Normalization utility: ensure language code is valid

def normalize_language_code(code: str) -> str:
    return LANGUAGE_CODES.get(code, 'en-US')

# Response parsing utilities (placeholders for actual boto3 response handling)

def parse_transcription_result(raw_response):
    # raw_response is a boto3 TranscribeStreamingEvent (JSON string)
    # Extract interim or final transcript parts
    try:
        event = json.loads(raw_response)
        results = event.get('results', [])
        transcript_parts = []
        for res in results:
            if res.get('is_final'):
                for alt in res.get('alternatives', []):
                    transcript_parts.append(alt.get('transcript'))
        return ' '.join(transcript_parts)
    except Exception as e:
        print('Failed to parse transcription response:', e)
        return ''

# Example helper to build a streaming request dict

def build_stream_request(language_code='en-US', sample_rate=16000, media_type='audio/l16', vocab_name=None):
    return {
        'LanguageCode': normalize_language_code(language_code),
        'MediaSampleRateHertz': sample_rate,
        'MediaType': media_type,
        'VocabularyName': vocab_name,
    }

# End of helper module
