import speech_client

def start_stream_with_language(language_code='en-US'):
    client = speech_client.get_streaming_client()
    config = client.create_config(language_code=language_code, enable_automatic_punctuation=True)
    return client.start_stream(config)
