import os
from speech_client import TextToSpeechClient  # Azure provider

def check_script_safety(text):
    # Placeholder: call content safety service (azur econtent safety, perspective, etc.)
    result = safety_check(text)
    return result['safe']

def safety_check(text):
    # Simulated safety check response; replace with actual API call (e.g., Azure Content Safety, Perspective API)
    return {'safe': True}
