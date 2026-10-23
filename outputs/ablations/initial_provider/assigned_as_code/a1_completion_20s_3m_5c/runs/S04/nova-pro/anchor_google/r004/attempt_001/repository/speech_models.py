from google.cloud.speech import types



def create_recognition_config(language_code, enable_speaker_diarization=False):
    return types.RecognitionConfig(
        language_code=language_code,
        enable_speaker_diarization=enable_speaker_diarization,
    )


def create_recognition_audio(uri):
    return types.RecognitionAudio(uri=uri)


def normalize_transcript(response):
    results = []
    for result in response.results:
        alternatives = result.alternatives
        if alternatives:
            transcript = alternatives[0].transcript
            results.append(transcript)
    return results