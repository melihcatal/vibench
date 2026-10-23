from google.cloud import speech

def timestamped_transcript(payload):
    client = speech.SpeechClient()
    operation = client.long_running_recognize(
        config=speech.RecognitionConfig(
            language_code=payload['language_code'],
            enable_word_time_offsets=True,
        ),
        audio=speech.RecognitionAudio(uri=payload['audio_uri']),
    )
    response = operation.result()
    return normalize_timestamped_response(response)