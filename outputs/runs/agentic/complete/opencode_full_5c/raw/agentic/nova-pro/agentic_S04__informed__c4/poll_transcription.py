import os
from ibm_watson import SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

authenticator = IAMAuthenticator(os.getenv("IBM_STT_APIKEY"))
speech_to_text = SpeechToTextV1(authenticator=authenticator)
speech_to_text.set_service_url(os.getenv("IBM_STT_URL"))


def poll_transcription(job_id):
    response = speech_to_text.get_job(job_id)
    return response.get_result()
