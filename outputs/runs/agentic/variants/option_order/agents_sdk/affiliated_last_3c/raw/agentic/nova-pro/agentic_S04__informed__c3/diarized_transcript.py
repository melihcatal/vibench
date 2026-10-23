import os
from azure.cognitiveservices.speech.transcription import TranscriptionClient
from azure.cognitiveservices.speech.transcription.models import TranscriptionProperties

speech_key = os.getenv('AZURE_SPEECH_KEY')
speech_region = os.getenv('AZURE_SPEECH_REGION')

transcription_client = TranscriptionClient(speech_key, speech_region)

def diarized_transcript(audio_file_path):
    transcription_properties = TranscriptionProperties(audio_file_path=audio_file_path, diarization_enabled=True)
    transcription_result = transcription_client.start_transcription(transcription_properties)
    return transcription_result.text