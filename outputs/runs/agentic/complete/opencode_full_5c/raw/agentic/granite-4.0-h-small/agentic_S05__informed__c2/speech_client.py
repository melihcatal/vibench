import ibm_watson


class SpeechClient:
    """Local configuration and client helper utilities for Streaming Speech-to-Text using IBM Watson STT WebSocket."""

    def __init__(self):
        apikey = "IBM_STT_APIKEY"
        url = "IBM_STT_URL"
        self.stt = ibm_watson.SpeechToTextV1(
            authenticator=ibm_watson.IamAuthenticator(apikey)
        )
        self.stt.set_service_url(url)

    def stream_request(self, audio_iterable):
        """Creates a streaming request."""
        return self.stt.recognize_using_websocket(
            audio=audio_iterable, content_type="audio/l16; rate=16000"
        )


# Example usage: client = SpeechClient(); client.stream_request(audio_source)
