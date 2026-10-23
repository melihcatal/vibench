import asyncio
from dashscope import AudioStreamingRecognize, credentials

# DashScope Real-time ASR
# provider: DashScope Real-time speech recognition


class StreamMicrophone:
    """Stream audio from the microphone and yield interim transcripts using DashScope.

    Configuration:
        DASHSCOPE_API_KEY must be set in the environment.
    """

    def __init__(self, language="en-US", punctuation=True):
        self.client = AudioStreamingRecognize()
        self.language = language
        self.punctuation = punctuation
        # configure credentials via environment variable
        credentials.set_api_key(credentials.ApiKey.from_env("DASHSCOPE_API_KEY"))

    async def start(self):
        """Start streaming recognition.

        Yields:
            str: partial transcript updates.
        """
        async for result in self.client.recognize_stream():
            if result.type == "partial":
                yield result.partial_result
            elif result.type == "final":
                yield result.final_result


if __name__ == "__main__":
    recognizer = StreamMicrophone(language="en-US")
    loop = asyncio.get_event_loop()
    async for transcript in recognizer.start():
        print("Transcript: ", transcript)
