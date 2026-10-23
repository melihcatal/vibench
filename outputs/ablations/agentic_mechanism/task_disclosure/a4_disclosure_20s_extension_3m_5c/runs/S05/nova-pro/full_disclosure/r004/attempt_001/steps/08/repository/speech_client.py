from google.cloud import speech_v1 as speech

def create_client(project_id: str):
    return speech.SpeechClient(project=project_id)

def get_config(language_code: str, encoding: str, sample_rate_hertz: int):
    config = speech.RecognitionConfig(
        encoding=encoding,
        sample_rate_hertz=sample_rate_hertz,
        language_code=language_code,
    )
    return config