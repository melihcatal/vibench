from google.cloud import speech_v1p1beta1 as speech
from google.oauth2 import service_account
import io
import os


def tts_qa_transcript(payload, config=None):
    config = config or {}
    
    # Authenticate using GOOGLE_APPLICATION_CREDENTIALS environment variable or service account info
    # if config.get('google_application_credentials_path'):
    #     os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = config['google_application_credentials_path']
    #     credentials = None
    # elif config.get('google_service_account_info'):
    #     credentials = service_account.Credentials.from_service_account_info(config['google_service_account_info'])
    #     client = speech.SpeechClient(credentials=credentials)
    # else:
    #     client = speech.SpeechClient() # Uses default credentials
    
    client = speech.SpeechClient() # For local development, assume GOOGLE_APPLICATION_CREDENTIALS is set up
    
    audio_bytes = payload['audio_bytes']
    language_code = payload.get('language_code', 'en-US')
    sample_rate_hertz = payload.get('sample_rate_hertz', 16000)
    audio_encoding = payload.get('audio_encoding', speech.RecognitionConfig.AudioEncoding.MP3) # Assuming MP3 from synthesize_text
    
    audio = speech.RecognitionAudio(content=audio_bytes)
    config_sr = speech.RecognitionConfig(
        encoding=audio_encoding,
        sample_rate_hertz=sample_rate_hertz,
        language_code=language_code,
    )
    
    response = client.recognize(config=config_sr, audio=audio)
    
    transcript = ""
    for result in response.results:
        transcript += result.alternatives[0].transcript
        
    return {'transcript': transcript}