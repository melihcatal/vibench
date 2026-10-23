import os

# ElevenLabs TTS client configuration
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

# Amazon Polly configuration (assume AWS credentials are set via env vars)
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")

# Google Cloud Text-to-Speech configuration (application credentials)
GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

# IBM Watson TTS configuration
IBM_TTS_APIKEY = os.getenv("IBM_TTS_APIKEY")
IBM_TTS_URL = os.getenv(
    "IBM_TTS_URL", "https://api.us-south.text-to-speech.watson.cloud.ibm.com"
)

# Azure Speech TTS configuration
AZURE_SPEECH_KEY = os.getenv("AZURE_SPEECH_KEY")
AZURE_SPEECH_REGION = os.getenv("AZURE_SPEECH_REGION", "eastus")

# Placeholder for other providers if needed
