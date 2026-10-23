import asyncio
from ibm_watson import SpeechToTextV1, RecognizeWithWebsocketsParams, AudioSource

# Watson Speech to Text WebSocket
# provider: Watson STT WebSocket


class PartialResultsHandler:
    """
    Handles WebSocket streaming partial and final recognition events.
    Configuration:
        IBM_STT_APIKEY and IBM_STT_URL must be set in the environment.
    """

    def __init__(self, language_model: str = "en-US_BroadbandModel"):
        self.service = SpeechToTextV1()
        self.service.set_apikey(credentials.ApiKey.from_env("IBM_STT_APIKEY"))
        self.service.set_service_url(credentials.ServiceUrl.from_env("IBM_STT_URL"))
        self.language_model = language_model

    async def stream(self, audio_file: str):
        """
        Streams audio from a file, yielding interim and final transcripts.
        Yields:
            dict: partial result with interim transcript
            dict: final result with final transcript
        """
        with open(audio_file, "rb") as audio_file_obj:
            audio = AudioSource(file=audio_file_obj)
            params = RecognizeWithWebsocketsParams(
                audio=audio,
                content_type="audio/l16; rate=44100",
                interim_results=True,
                language_model=self.language_model,
            )

            async for result in self.service.recognize_using_websocket(params):
                if result.is_partial:
                    yield {
                        "type": "interim",
                        "transcript": result.result["results"][0]["alternatives"][0][
                            "transcript"
                        ],
                    }
                else:
                    yield {
                        "type": "final",
                        "transcript": result.result["results"][0]["alternatives"][0][
                            "transcript"
                        ],
                    }


if __name__ == "__main__":
    handler = PartialResultsHandler()
    loop = asyncio.get_event_loop()
    async for event in handler.stream("sample.wav"):
        print(event)
