from google.cloud import speech

def stream_with_language(audio_chunks, language_code='en-US', punctuation=True):
    config = {
        'language_code': language_code,
        'enable_automatic_punctuation': punctuation
    }
    return stream_chunks(audio_chunks, config=config)
