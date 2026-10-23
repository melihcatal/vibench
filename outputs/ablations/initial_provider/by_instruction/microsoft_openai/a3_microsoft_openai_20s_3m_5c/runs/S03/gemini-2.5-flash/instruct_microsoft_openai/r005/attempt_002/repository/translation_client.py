import os
from openai import OpenAI
# from google.cloud import translate
# import boto3
# import deepl
# from azure.cognitiveservices.vision.contentmoderator import ContentModeratorClient
# import cohere

def get_openai_client():
    # OpenAI API key should be set as an environment variable OPENAI_API_KEY
    return OpenAI()

# def get_google_translate_client():
#     return translate.TranslationServiceClient()

# def get_aws_translate_client():
#     return boto3.client('translate')

# def get_deepl_client():
#     auth_key = os.environ.get("DEEPL_AUTH_KEY")
#     return deepl.Translator(auth_key)

# def get_azure_content_moderator_client():
#     subscription_key = os.environ.get('AZURE_CONTENT_MODERATOR_SUBSCRIPTION_KEY')
#     endpoint = os.environ.get('AZURE_CONTENT_MODERATOR_ENDPOINT')
#     return ContentModeratorClient(endpoint, CognitiveServicesCredentials(subscription_key))

# def get_cohere_client():
#     api_key = os.environ.get("COHERE_API_KEY")
#     return cohere.Client(api_key)

# def get_google_text_to_speech_client():
#     from google.cloud import texttospeech
#     return texttospeech.TextToSpeechClient()
