import os
import azure.cognitiveservices.speech as speechsdk
from google.cloud import speech_v1p1beta1 as speech_google
import boto3
from ibm_watson import SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

def get_azure_speech_recognizer():
    speech_config = speechsdk.SpeechConfig(
        subscription=os.environ.get("SPEECH_KEY"), 
        region=os.environ.get("SPEECH_REGION")
    )
    audio_config = speechsdk.AudioConfig(use_microphone=True)
    return speechsdk.SpeechRecognizer(
        speech_config=speech_config, 
        audio_config=audio_config
    )

def get_google_speech_client():
    return speech_google.SpeechClient()

def get_aws_transcribe_client():
    return boto3.client(
        "transcribe",
        region_name=os.environ.get("AWS_REGION"),
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY")
    )

def get_watson_speech_to_text_client():
    authenticator = IAMAuthenticator(os.environ.get("WATSON_SPEECH_TO_TEXT_APIKEY"))
    speech_to_text = SpeechToTextV1(
        authenticator=authenticator
    )
    speech_to_text.set_service_url(os.environ.get("WATSON_SPEECH_TO_TEXT_URL"))
    return speech_to_text
