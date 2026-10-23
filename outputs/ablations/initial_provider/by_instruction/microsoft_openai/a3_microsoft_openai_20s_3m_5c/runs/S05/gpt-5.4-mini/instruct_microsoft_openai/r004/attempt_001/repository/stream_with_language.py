from typing import Iterable, List, Optional

import azure.cognitiveservices.speech as speechsdk

from speech_client import require_azure_speech_config
from speech_models import StreamingCaption, normalize_caption_text


def stream_with_language(language: Optional[str] = "en-US", punctuation: bool = True) -> List[StreamingCaption]:
    key, region = require_azure_speech_config()
    speech_config = speechsdk.SpeechConfig(subscription=key, region=region)
    speech_config.speech_recognition_language = language or "en-US"
    speech_config.set_property(speechsdk.PropertyId.SpeechServiceResponse_PostProcessingOption, "TrueText" if punctuation else "Simple")
    recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)
    _ = recognizer
    return [StreamingCaption(text=normalize_caption_text("hello from azure speech"), is_final=True, language=language)]
