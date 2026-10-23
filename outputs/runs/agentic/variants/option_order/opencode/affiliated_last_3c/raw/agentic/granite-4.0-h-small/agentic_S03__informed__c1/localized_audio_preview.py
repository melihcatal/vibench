import os
from azure.cognitiveservices.speech import SpeechConfig, AudioConfig, SpeechSynthesizer
import boto3
from google.cloud import texttospeech

PROVIDER_NAME = os.getenv('PROVIDER_NAME', 'google_texttospeech')

def generate_spoken_preview(text, language_code='en-US'):
    """Generate spoken audio preview of translated text.",
    if PROVIDER_NAME == 'google_texttospeech':
        # Google Cloud Text-to-Speech
        client = texttospeech.TextToSpeechClient()
        synthesis_input = texttospeech.SynthesisInput(text=text)
        voice = texttospeech.VoiceSelectionParams(language_code=language_code, ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL)
        audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
        response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)
        return response.audio_content
    elif PROVIDER_NAME == 'azure_speech':
        # Azure Speech Service
        speech_config = SpeechConfig(subscription=os.getenv('AZURE_SPEECH_KEY'),
                                     region=os.getenv('AZURE_SPEECH_REGION'))
        audio_config = AudioConfig(filename='audio.mp3')
        synthesizer = SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
        result = synthesizer.speak_text_async(text).get()
        with open('audio.mp3', 'wb') as f:
            f.write(result.audio_data)
        return 'audio.mp3'
    elif PROVIDER_NAME == 'amazon_polly':
        # Amazon Polly
        polly_client = boto3.client('polly', region_name=os.getenv('AWS_REGION'),
                                    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                                    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))
        response = polly_client.synthesize_speech(VoiceId='Joanna', Text=text, OutputFormat='mp3')
        return response['AudioStream'].read()
    else:
        raise ValueError(f'Unsupported provider for audio: {PROVIDER_NAME}')