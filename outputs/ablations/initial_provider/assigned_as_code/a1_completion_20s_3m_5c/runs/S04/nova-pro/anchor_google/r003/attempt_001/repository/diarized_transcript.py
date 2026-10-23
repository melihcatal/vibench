from google.cloud import speech

def diarized_transcript(payload):
    client = speech.SpeechClient()
    operation = client.long_running_recognize(
        config=speech.RecognitionConfig(
            language_code=payload['language_code'],
            enable_speaker_diarization=True,
        ),
        audio=speech.RecognitionAudio(uri=payload['audio_uri']),
    )
    response = operation.result()
    return normalize_diarization_response(response)