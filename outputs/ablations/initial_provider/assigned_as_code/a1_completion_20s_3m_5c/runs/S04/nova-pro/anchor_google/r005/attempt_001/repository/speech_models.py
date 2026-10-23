from google.cloud import speech


def normalize_request(payload):
    return {
        "config": speech.RecognitionConfig(
            language_code=payload["language_code"]
        ),
        "audio": speech.RecognitionAudio(uri=payload["audio_uri"])
    }


def normalize_response(response):
    return {
        "transcript": response.results[0].alternatives[0].transcript,
        "timestamps": response.results[0].alternatives[0].words
    }