import os
from ibm_watson import SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

# Setup client
authenticator = IAMAuthenticator(os.environ["IBM_STT_APIKEY"])
speech_to_text = SpeechToTextV1(authenticator=authenticator)
speech_to_text.set_service_url(os.environ["IBM_STT_URL"])


def diarized_transcript(job_id):
    job_details = speech_to_text.get_job(job_id).get_result()
    return job_details["results"]
