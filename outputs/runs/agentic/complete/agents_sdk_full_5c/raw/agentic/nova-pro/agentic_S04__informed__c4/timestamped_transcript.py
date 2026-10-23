import os
from ibm_watson import SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

def timestamped_transcript(file_path):
    apikey = os.environ.get('IBM_STT_APIKEY')
    url = os.environ.get('IBM_STT_URL')
    authenticator = IAMAuthenticator(apikey)
    speech_to_text = SpeechToTextV1(authenticator=authenticator)
    speech_to_text.set_service_url(url)
    with open(file_path, 'rb') as audio_file:
        result = speech_to_text.recognize(
            audio=audio_file,
            content_type='audio/wav',
            timestamps=True,
            word_alternatives_threshold=0.01
        ).get_result()
        return result