from google.cloud import speech_v1
from google.cloud.speech_v1 import enums
from google.auth import default

def create_speech_client():
    credentials, project = default()
    client = speech_v1.SpeechClient(credentials=credentials)
    return client

def create_batch_config(config_name, audio_file_path):
    config = {
        'encoding': enums.RecognitionConfig.AudioEncoding.LINEAR16,
        'sample_rate_hertz': 16000,
        'language_code': 'en-US',
    }
    audio = {
        'uri': audio_file_path,
    }
    return {
        'config': config,
        'audio': audio,
        'output_config': {
            'gcs_uri': f'gs://{config_name}/output'
        }
    }