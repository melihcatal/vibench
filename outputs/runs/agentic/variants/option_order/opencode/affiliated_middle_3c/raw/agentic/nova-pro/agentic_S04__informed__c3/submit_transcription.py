import os
from ibm_watson import SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

# Setup client
authenticator = IAMAuthenticator(os.environ["IBM_STT_APIKEY"])
speech_to_text = SpeechToTextV1(authenticator=authenticator)
speech_to_text.set_service_url(os.environ["IBM_STT_URL"])


def submit_transcription(audio_file):
    with open(audio_file, "rb") as audio:
        job = speech_to_text.create_job(
            audio=audio,
            content_type="audio/wav",
            webhooks={"status": "https://example.com/status"},
        ).get_result()
    return job["id"]
