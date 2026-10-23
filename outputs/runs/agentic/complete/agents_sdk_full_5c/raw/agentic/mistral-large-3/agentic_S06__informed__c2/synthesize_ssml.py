from typing import Iterator
import os
from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from speech_client import get_speech_client
from speech_models import SynthesisRequest, SynthesisResponse


def synthesize_ssml(request: SynthesisRequest) -> Iterator[bytes]:
    authenticator = IAMAuthenticator(os.getenv("IBM_TTS_APIKEY"))
    client = TextToSpeechV1(authenticator=authenticator)
    client.set_service_url(os.getenv("IBM_TTS_URL"))

    response = client.synthesize(
        request.text,
        accept="audio/wav",
        ssml=request.ssml_enabled
    ).get_result()

    yield from SynthesisResponse(audio=response.content).audio_chunks()