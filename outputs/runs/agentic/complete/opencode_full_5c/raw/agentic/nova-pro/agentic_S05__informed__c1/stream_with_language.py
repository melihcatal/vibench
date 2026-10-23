import asyncio
from ibm_watson import SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator


async def stream_with_language():
    authenticator = IAMAuthenticator(os.getenv("IBM_STT_APIKEY"))
    speech_to_text = SpeechToTextV1(authenticator=authenticator)
    speech_to_text.set_service_url(os.getenv("IBM_STT_URL"))
    async for transcript in speech_to_text.recognize_using_websocket(
        audio=b"audio_chunk",
        content_type="audio/wav",
        language_customization_id="en-US_BroadbandModel",
    ):
        yield transcript


asyncio.run(stream_with_language())
