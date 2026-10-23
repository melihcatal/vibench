import os
from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

os.environ["IBM_TTS_APIKEY"] = "your-api-key"
os.environ["IBM_TTS_URL"] = "your-url"
authenticator = IAMAuthenticator(os.environ["IBM_TTS_APIKEY"])
tts = TextToSpeechV1(authenticator=authenticator)
tts.set_service_url(os.environ["IBM_TTS_URL"])
