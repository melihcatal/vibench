import os
import assemblyai as aai


def get_speech_client():
    aai.settings.api_key = os.getenv("ASSEMBLYAI_API_KEY")
    return aai
