import os
from ibm_watson import SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from speech_client import get_speech_client
from speech_models import StreamingRecognitionConfig


def start_streaming_recognizer(
    language: str = "en-US", enable_punctuation: bool = True, model: str = None
) -> StreamingRecognitionConfig:
    """
    Starts a streaming recognizer with language and punctuation settings for IBM Watson STT.
    """
    authenticator = IAMAuthenticator(os.getenv("IBM_STT_APIKEY"))
    speech_client = SpeechToTextV1(authenticator=authenticator)
    speech_client.set_service_url(os.getenv("IBM_STT_URL"))

    model_id = model or f"{language}_Multimedia"
    if language.startswith("zh-"):
        model_id = f"{language}_Telephony"
    elif language.startswith("ar-"):
        model_id = f"{language}_Multimedia"

    config = StreamingRecognitionConfig(
        model=model_id,
        interim_results=True,
        smart_formatting=enable_punctuation,
        content_type="audio/l16; rate=44100",
    )

    return config
