from google.cloud import speech_v1p1beta1 as speech

def build_streaming_recognize_request(audio_content: bytes = None, streaming_config: speech.StreamingRecognitionConfig = None):
    """Builds a StreamingRecognizeRequest."""
    if streaming_config:
        return speech.StreamingRecognizeRequest(streaming_config=streaming_config)
    elif audio_content:
        return speech.StreamingRecognizeRequest(audio_content=audio_content)
    return speech.StreamingRecognizeRequest()
