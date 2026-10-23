import os
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types

# Initialize the Google Cloud Speech client
speech_client = speech.SpeechClient()