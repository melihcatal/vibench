import os
import azure.cognitiveservices.speech as speechsdk

def get_speech_recognizer_client():
    speech_key = os.environ.get("AZURE_SPEECH_KEY")
    service_region = os.environ.get("AZURE_SPEECH_REGION")

    if not speech_key or not service_region:
        raise ValueError("AZURE_SPEECH_KEY and AZURE_SPEECH_REGION environment variables must be set.")

    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    # This client is for real-time, for batch, we'll use a different approach with REST API or batch client.
    # For now, this serves as a placeholder for provider identification.
    return speech_config

def get_batch_transcription_client():
    # In a real scenario, this would involve Azure's Speech service REST API for batch transcription.
    # For provider identification, we'll use the environment variables here.
    speech_key = os.environ.get("AZURE_SPEECH_KEY")
    service_region = os.environ.get("AZURE_SPEECH_REGION")
    if not speech_key or not service_region:
        raise ValueError("AZURE_SPEECH_KEY and AZURE_SPEECH_REGION environment variables must be set.")
    # This function would return a client object capable of interacting with the batch transcription API.
    # For simplicity and provider identification, we'll just return the config for now.
    return {
        "key": speech_key,
        "region": service_region,
        "endpoint": f"https://{service_region}.api.cognitive.microsoft.com/speechtotext/v3.1"
    }
