import os
import assemblyai as aai

aai.settings.api_key = os.getenv("ASSEMBLYAI_API_KEY")


def get_transcriber():
    return aai.Transcriber()
