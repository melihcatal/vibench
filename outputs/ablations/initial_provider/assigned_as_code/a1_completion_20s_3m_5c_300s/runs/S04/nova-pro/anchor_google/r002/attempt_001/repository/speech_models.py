from google.cloud import speech


def normalize_transcription_response(response):
    return {
        "transcript": response.results[0].alternatives[0].transcript,
        "confidence": response.results[0].alternatives[0].confidence,
    }