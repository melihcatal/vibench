from ibm_watson import SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

authenticator = IAMAuthenticator("IBM_STT_APIKEY")
speech_to_text = SpeechToTextV1(authenticator=authenticator)
speech_to_text.set_service_url("IBM_STT_URL")


def poll_transcription(job_id):
    job_details = speech_to_text.get_job(job_id).get_result()
    if job_details["status"] == "completed":
        return speech_to_text.get_job_results(job_id).get_result()["results"]
    else:
        return None
