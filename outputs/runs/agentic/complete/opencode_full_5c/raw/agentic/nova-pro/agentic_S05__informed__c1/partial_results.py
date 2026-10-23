import asyncio
from ibm_watson import SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator


async def partial_results():
    authenticator = IAMAuthenticator(os.getenv("IBM_STT_APIKEY"))
    speech_to_text = SpeechToTextV1(authenticator=authenticator)
    speech_to_text.set_service_url(os.getenv("IBM_STT_URL"))
    async for transcript in speech_to_text.recognize_using_websocket(
        audio=b"audio_chunk", content_type="audio/wav"
    ):
        if transcript["results"][0]["final"]:
            yield transcript["results"][0]["alternatives"][0]["transcript"]


asyncio.run(partial_results())
