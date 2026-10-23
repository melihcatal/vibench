from ibm_watson import SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

authenticator = IAMAuthenticator("IBM_STT_APIKEY")
speech_to_text = SpeechToTextV1(authenticator=authenticator)
speech_to_text.set_service_url("IBM_STT_URL")


def diarized_transcript(audio_file):
    with open(audio_file, "rb") as audio:
        job = speech_to_text.create_job(
            audio,
            content_type="audio/mp3",
            customization_id="YOUR_CUSTOMIZATION_ID",
            speaker_labels=True,
        )
        return job.get_result()["id"]
