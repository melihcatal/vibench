import os
import os

def get_speech_config():
    speech_key = os.environ.get("SPEECH_KEY")
    speech_region = os.environ.get("SPEECH_REGION")
    return speech_key, speech_region
