from google.cloud import speech

def get_speech_client():
    return speech.SpeechClient()

def create_recognition_config(language_code, enable_speaker_diarization=False):
    return speech.RecognitionConfig(
        language_code=language_code,
        enable_speaker_diarization=enable_speaker_diarization,
    )

def create_recognition_audio(uri):
    return speech.RecognitionAudio(uri=uri)